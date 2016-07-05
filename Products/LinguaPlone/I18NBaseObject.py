from zope.event import notify
from zope.interface import implementer
from zope.site.hooks import getSite

from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from Acquisition import aq_inner
from Acquisition import aq_parent
from App.class_init import InitializeClass
from OFS.ObjectManager import BeforeDeleteException
from OFS.CopySupport import CopyError
from Products.Archetypes.atapi import BaseObject
from Products.Archetypes.config import LANGUAGE_DEFAULT
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.Archetypes.config import UID_CATALOG
from Products.Archetypes.interfaces import IMultiPageSchema
from Products.Archetypes.utils import mapply
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DynamicType import DynamicType
from Products.CMFDynamicViewFTI.interface import ISelectableBrowserDefault
from Products.ZCatalog.Lazy import LazyMap

from Products.LinguaPlone import config
from Products.LinguaPlone import events
from Products.LinguaPlone import permissions
from Products.LinguaPlone.config import RELATIONSHIP
from Products.LinguaPlone.utils import isInitialTranslationId
from Products.LinguaPlone.interfaces import ILocateTranslation
from Products.LinguaPlone.interfaces import ITranslatable
from Products.LinguaPlone.interfaces import ITranslationFactory

import logging
log = logging.getLogger(__name__)

_marker = object()


class AlreadyTranslated(Exception):
    """Raised when trying to create an existing translation."""
    pass


class TypeInfoWrapper:
    """Wrapper around typeinfo, used for the override of getTypeInfo
    used to intercept the edit alias and display translation form"""
    security = ClassSecurityInfo()

    def __init__(self, typeinfo, contentitem):
        self.__typeinfo = typeinfo
        self.__contentitem = contentitem

    def __nonzero__(self):
        return bool(self.__typeinfo)

    security.declarePublic('getActionInfo')
    def getActionInfo(self, action_chain, object=None, check_visibility=0,
            check_condition=0):
        res = self.__typeinfo.getActionInfo(action_chain, object,
                check_visibility, check_condition)
        if action_chain=='object/edit':
            urlparts=res['url'].split('/')
            if (urlparts[-1] in [('atct_edit', 'base_edit')]
                    and not self.__contentitem.isCanonical()):
                urlparts[-1]='translate_item'
                res['url']='/'.join(urlparts)
        return res

    security.declarePublic('queryMethodID')
    def queryMethodID(self, alias, default=None, context=None):
        if alias == 'edit':
            res = self.__typeinfo.queryMethodID(alias, default, context)
            if (res in ('atct_edit', 'base_edit')
                    and not self.__contentitem.isCanonical()):
                return 'translate_item'
        return self.__typeinfo.queryMethodID(alias, default, context)

    def __getattr__(self, value):
        return getattr(self.__typeinfo, value)


@implementer(ITranslatable)
class I18NBaseObject(Implicit):
    """Base class for translatable objects."""

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'isTranslation')
    def isTranslation(self):
        """Tells whether this object is used in a i18n context."""
        return bool(self.getReferenceImpl(RELATIONSHIP) or \
                    self.getBackReferenceImpl(RELATIONSHIP) \
                    and self.Language() or False)

    security.declareProtected(permissions.AddPortalContent, 'addTranslation')
    def addTranslation(self, language, *args, **kwargs):
        """Adds a translation."""
        if self.hasTranslation(language):
            translation = self.getTranslation(language)
            raise AlreadyTranslated(translation.absolute_url())

        locator = ILocateTranslation(self)
        parent = locator.findLocationForTranslation(language)

        notify(events.ObjectWillBeTranslatedEvent(self, language))

        canonical = self.getCanonical()
        kwargs[config.KWARGS_TRANSLATION_KEY] = canonical

        factory = ITranslationFactory(self)
        translation = factory.createTranslation(
            parent, language, *args, **kwargs)
        translation.reindexObject()
        notify(events.ObjectTranslatedEvent(self, translation, language))

        return translation


    security.declareProtected(permissions.AddPortalContent,
                              'addTranslationReference')
    def addTranslationReference(self, translation):
        """Adds the reference used to keep track of translations."""
        if self.hasTranslation(translation.Language()):
            double = self.getTranslation(translation.Language())
            raise AlreadyTranslated(double.absolute_url())
        self.addReference(translation, RELATIONSHIP)

    security.declareProtected(permissions.ModifyPortalContent,
                              'removeTranslation')
    def removeTranslation(self, language):
        """Removes a translation, pass on to layer."""
        translation = self.getTranslation(language)
        if translation.isCanonical():
            self.setCanonical()
        translation_parent = aq_parent(aq_inner(translation))
        translation_parent.manage_delObjects([translation.getId()])

    security.declareProtected(permissions.ModifyPortalContent,
                              'removeTranslationReference')
    def removeTranslationReference(self, translation):
        """Removes the translation reference."""
        translation.deleteReference(self, RELATIONSHIP)

    security.declareProtected(permissions.View, 'hasTranslation')
    def hasTranslation(self, language):
        """Checks if a given language has a translation."""
        return language in self.getTranslationLanguages()

    security.declareProtected(permissions.View, 'getTranslation')
    def getTranslation(self, language=None):
        """Gets a translation, pass on to layer."""
        if language is None:
            language_tool = getToolByName(self, 'portal_languages', None)
            if language_tool is not None:
                language = language_tool.getPreferredLanguage()
            else:
                return self
        # Short-cut for self
        lang = self.Language()
        if lang == language:
            return self
        # Find and test canonical
        canonical = self
        if not self.isCanonical():
            canonical = self.getCanonical()
        if canonical.Language() == language:
            return canonical
        brains = canonical.getTranslationBackReferences()
        if brains:
            found = [b for b in brains if b.Language == language]
            if found:
                return self._getReferenceObject(uid=found[0].sourceUID)
        return None

    security.declareProtected(permissions.View, 'getTranslationLanguages')
    def getTranslationLanguages(self):
        """Returns a list of language codes.

        Note that we return all translations available. If you want only
        the translations from the current portal_language selected list,
        you should use the getTranslatedLanguages script.
        """
        canonical = self
        if not self.isCanonical():
            canonical = self.getCanonical()
        brains = canonical.getTranslationBackReferences()
        result = [canonical.Language()]
        result.extend([b.Language for b in brains])
        return result

    security.declareProtected(permissions.View, 'getTranslations')
    def getTranslations(self, include_canonical=True, review_state=True,
                        _is_canonical=None):
        """Returns a dict of {lang : [object, wf_state]}.
        If review_state is False, returns a dict of {lang : object}
        """
        if _is_canonical is None:
            _is_canonical = self.isCanonical()
        if _is_canonical:
            result = {}
            lang = self.Language()
            state = None
            workflow_tool = getToolByName(self, 'portal_workflow', None)
            if workflow_tool is None:
                # No context, most likely FTP or WebDAV
                if review_state:
                    return {lang: [self, None]}
                else:
                    return {lang: self}
            if review_state:
                state = workflow_tool.getInfoFor(self, 'review_state', None)
            if include_canonical:
                if review_state:
                    result[lang] = [self, state]
                else:
                    result[lang] = self
            for obj in self.getTranslationBackReferences(objects=True):
                if obj is None:
                    continue
                lang = obj.Language()
                state = None
                if review_state:
                    state = workflow_tool.getInfoFor(obj, 'review_state', None)
                    result[lang] = [obj, state]
                else:
                    result[lang] = obj
            return result
        else:
            _canonical = self.getCanonical()
            if _canonical is None:
                return {}
            else:
                return _canonical.getTranslations(
                    include_canonical=include_canonical,
                    review_state=review_state,
                    _is_canonical=True)

    security.declareProtected(permissions.View, 'getNonCanonicalTranslations')
    def getNonCanonicalTranslations(self):
        """Returns a dict of {lang : [object, wf_state]}."""
        return self.getTranslations(include_canonical=False)

    security.declareProtected(permissions.View, 'isCanonical')
    def isCanonical(self):
        """Tells whether this is the canonical translation.

        An object is considered 'canonical' when there's no
        'translationOf' references associated.
        """
        return not bool(self.getTranslationReferences())

    security.declareProtected(permissions.ModifyPortalContent, 'setCanonical')
    def setCanonical(self):
        """Sets the canonical attribute."""
        if not self.isCanonical():
            translations = self.getTranslations(
                _is_canonical=False, review_state=False).values()
            for obj in translations:
                obj.deleteReferences(RELATIONSHIP)
            for obj in translations:
                if obj != self:
                    obj.addTranslationReference(self)

    security.declareProtected(permissions.View, 'getCanonicalLanguage')
    def getCanonicalLanguage(self):
        """Returns the language code for the canonical language."""
        return self.getCanonical().Language()

    security.declareProtected(permissions.View, 'getCanonical')
    def getCanonical(self):
        """Returns the canonical translation."""
        ret = self
        refs = self.getTranslationReferences()
        if len(refs):
            ret = self._getReferenceObject(uid=refs[0].targetUID)
        return ret

    security.declareProtected(permissions.View, 'getLanguage')
    def getLanguage(self):
        """Returns the language code."""
        return self.Language()

    security.declareProtected(permissions.ModifyPortalContent, 'setLanguage')
    def setLanguage(self, value, **kwargs):
        """Sets the language code.

        When changing the language in a translated folder structure,
        we try to move the content to the existing language tree.
        """
        # If we are called during a schema update we should not be
        # deleting any language relations or complaining about already
        # existing translations.  A schema update saves the current
        # value, sets the default language (at which point there can
        # easily be two English translations if that is the default
        # language) and restores the original value again.  So really
        # there is no reason for doing anything other than setting the
        # value.
        value = value or ''
        req = getattr(self, 'REQUEST', None)
        if shasattr(req, 'get'):
            if req.get('SCHEMA_UPDATE', None) is not None:
                # We at least should set the field.
                self.getField('language').set(self, value, **kwargs)
                return

        translation = self.getTranslation(value)
        if self.hasTranslation(value):
            if translation == self:
                return
            else:
                raise AlreadyTranslated(translation.absolute_url())
        self.getField('language').set(self, value, **kwargs)

        if not value:
            self.deleteReferences(RELATIONSHIP)

        parent = aq_parent(aq_inner(self))

        locator = ILocateTranslation(self)
        new_parent = locator.findLocationForTranslation(value)

        if new_parent != parent:
            try:
                info = parent.manage_cutObjects([self.getId()])
                new_parent.manage_pasteObjects(info)
            except CopyError:
                log.warning("Inconsistent translation for: %s" % repr(self))
        self.reindexObject()
        self._catalogRefs(self)

    security.declarePrivate('defaultLanguage')
    def defaultLanguage(self):
        """Returns the initial default language."""
        parent = aq_parent(aq_inner(self))
        if getattr(parent, 'portal_type', None) == 'TempFolder':
            # We have factory tool
            parent = aq_parent(aq_parent(parent))
        if ITranslatable.providedBy(parent):
            return parent.Language()

        language_tool = getToolByName(self, 'portal_languages', None)
        if language_tool:
            if language_tool.startNeutral():
                return ''
            else:
                return language_tool.getPreferredLanguage()
        else:
            return LANGUAGE_DEFAULT

    security.declarePrivate('_processForm')
    def _processForm(self, data=1, metadata=None, REQUEST=None, values=None):
        request = REQUEST or self.REQUEST
        if values:
            form = values
        else:
            form = request.form
        fieldset = form.get('fieldset', None)
        schema = self.Schema()
        schemata = self.Schemata()
        fields = []

        if not IMultiPageSchema.providedBy(self):
            fields = schema.fields()
        elif fieldset is not None:
            fields = schemata[fieldset].fields()
        else:
            if data:
                fields += schema.filterFields(isMetadata=0)
            if metadata:
                fields += schema.filterFields(isMetadata=1)

        canonical = self.isCanonical()
        for field in fields:
            if not canonical:
                # On non-canonical items the translate screen shows language
                # independent fields in view mode. This means the form will not
                # contain their data. The contract for processForm is that
                # missing fields can be interpreted as "delete all". We need to
                # avoid this for LP or we might accidentally delete data.
                if getattr(field, 'languageIndependent', False):
                    continue

            # Delegate to the widget for processing of the form
            # element.  This means that if the widget needs _n_
            # fields under a naming convention it can handle this
            # internally.  The calling API is process_form(instance,
            # field, form) where instance should rarely be needed,
            # field is the field object and form is the dict. of
            # kv_pairs from the REQUEST
            #
            # The product of the widgets processing should be:
            #   (value, **kwargs) which will be passed to the mutator
            #   or None which will simply pass

            if not field.writeable(self):
                # If the field has no 'w' in mode, or the user doesn't
                # have the required permission, or the mutator doesn't
                # exist just bail out.
                continue

            try:
                # Pass validating=False to inform the widget that we
                # aren't in the validation phase, IOW, the returned
                # data will be forwarded to the storage
                result = field.widget.process_form(self, field, form,
                                                   empty_marker=_marker,
                                                   validating=False)
            except TypeError:
                # Support for old-style process_form methods
                result = field.widget.process_form(self, field, form,
                                                   empty_marker=_marker)

            if result is _marker or result is None:
                continue

            # Set things by calling the mutator
            mutator = field.getMutator(self)
            __traceback_info__ = (self, field, mutator)
            result[1]['field'] = field.__name__
            mapply(mutator, result[0], **result[1])

        self.reindexObject()

    security.declarePrivate('_isIDAutoGenerated')
    def _isIDAutoGenerated(self, id):
        if not self.isCanonical():
            canonical_id = self.getCanonical().getId()
            language = self.Language()
            return isInitialTranslationId(id, canonical_id, language)
        return super(I18NBaseObject, self)._isIDAutoGenerated(id)

    security.declareProtected(permissions.ModifyPortalContent, 'processForm')
    def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
        """Process the schema looking for data in the form."""
        is_new_object = self.checkCreationFlag()
        BaseObject.processForm(self, data=data, metadata=metadata,
                               REQUEST=REQUEST, values=values)
        # LP specific bits
        if config.AUTO_NOTIFY_CANONICAL_UPDATE:
            if self.isCanonical():
                self.invalidateTranslations()

        # Check if an explicit id has been passed
        explicit_id = False
        if REQUEST is None:
            REQUEST = getattr(self, 'REQUEST', None)

        if REQUEST is not None:
            if 'id' in REQUEST.form and REQUEST.form.get('id'):
                explicit_id = True

        if values is not None:
            if 'id' in values and values.get('id'):
                explicit_id = True

        if (is_new_object and not explicit_id and
            self._at_rename_after_creation):
            # Renames an object like its normalized title
            self._renameAfterCreation(check_auto_id=True)

        if shasattr(self, '_lp_default_page'):
            delattr(self, '_lp_default_page')
            language = self.Language()
            parent = aq_parent(aq_inner(self))
            if ITranslatable.providedBy(parent) and parent.Language() != '':
                if not parent.hasTranslation(language):
                    parent.addTranslation(language)
                    translation_parent = parent.getTranslation(language)
                    translation_parent.processForm(
                            values=dict(title=self.Title()))
                    translation_parent.setDescription(self.Description())
                    parent = translation_parent

                if ISelectableBrowserDefault.providedBy(parent):
                    parent.setDefaultPage(self.getId())

        if shasattr(self, '_lp_outdated'):
            delattr(self, '_lp_outdated')

    security.declareProtected(
        permissions.ModifyPortalContent, 'invalidateTranslations')
    def invalidateTranslations(self):
        """Outdates all translations except the canonical one."""
        translations = self.getTranslations(
            include_canonical=False, review_state=False).values()
        for obj in translations:
            obj.notifyCanonicalUpdate()

    security.declarePrivate('notifyCanonicalUpdate')
    def notifyCanonicalUpdate(self):
        """Marks the translation as outdated."""
        self._lp_outdated = True
        # Because language independent fields may have changed, reindex
        self.reindexObject()
        self._catalogRefs(self)

    security.declareProtected(permissions.View, 'isOutdated')
    def isOutdated(self):
        """Checks if the translation is outdated."""
        return getattr(self, '_lp_outdated', False)

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        # Called from manage_beforeDelete() of subclasses to
        # veto deletion of the canonical translation object.
        if config.CANONICAL_DELETE_PROTECTION:
            if self.isCanonical() and self.getTranslationBackReferences():
                raise BeforeDeleteException('Delete translations first.')

    # Wrapper around typeinfo to hook into the edit alias
    security.declareProtected(
        permissions.AccessContentsInformation, 'getTypeInfo')
    def getTypeInfo(self):
        """Get the TypeInformation object specified by the portal type,
        possibly wrapped to intercept the edit alias.
        """
        ti = DynamicType.getTypeInfo(self)
        if ti is not None:
            return TypeInfoWrapper(ti, self)
        return ti

    security.declareProtected(permissions.View, 'getTranslationReferences')
    def getTranslationReferences(self, objects=False):
        """Get all translation references for this object"""
        brains = self._queryBrains('sourceUID')
        if brains:
            if objects:
                return [self._getReferenceObject(brain.targetUID)
                        for brain in brains]
            else:
                return brains
        return []

    security.declareProtected(permissions.View, 'getTranslationBackReferences')
    def getTranslationBackReferences(self, objects=False):
        """Get all translation back references for this object"""
        brains = self._queryBrains('targetUID')
        if brains:
            if objects:
                return [self._getReferenceObject(brain.sourceUID)
                        for brain in brains]
            else:
                return brains
        return []

    def _queryBrains(self, indexname):
        value = self.UID()
        if value is None:
            return []

        site = getSite()
        tool = getToolByName(site, REFERENCE_CATALOG)

        _catalog = tool._catalog
        indexes = _catalog.indexes

        # First get one or multiple record ids for the source/target uid index
        rids = indexes[indexname]._index.get(value, None)
        if rids is None:
            return []
        elif isinstance(rids, int):
            rids = [rids]
        else:
            rids = list(rids)

        # As a second step make sure we only get references of the right type
        # The unindex holds data of the type: [(-311870037, 'translationOf')]
        # The index holds data like: [('translationOf', -311870037)]
        # In a LinguaPlone site the index will have all content items indexed
        # so querying it is bound to be extremely slow
        rel_unindex_get = indexes['relationship']._unindex.get
        result_rids = set()
        for r in rids:
            rels = rel_unindex_get(r, None)
            if isinstance(rels, str) and rels == RELATIONSHIP:
                result_rids.add(r)
            elif RELATIONSHIP in rels:
                result_rids.add(r)

        # Create brains
        brains = LazyMap(_catalog.__getitem__,
                         list(result_rids), len(result_rids))
        return brains

    def _getReferenceObject(self, uid):
        tool = getToolByName(self, UID_CATALOG, None)
        brains = tool(UID=uid)
        for brain in brains:
            obj = brain.getObject()
            if obj is not None:
                return obj
        return None

    def setDefaultPage(self, objectId):
        """Reindex the default page status
           of old and new default page translations too
        """
        new_page = old_page = None
        if objectId is not None:
            new_page = getattr(self, objectId, None)

        if self.hasProperty('default_page'):
            pages = self.getProperty('default_page','')
            if isinstance(pages, (list, tuple)):
                for page in pages:
                    old_page = getattr(self, page, None)
                    if page is not None: break
            elif isinstance(pages, str):
                old_page = getattr(self, pages, None)

        super(I18NBaseObject, self).setDefaultPage(objectId)

        if new_page != old_page:
            if new_page is not None:
                for tr in new_page.getTranslations(review_state=False).values():
                    tr.reindexObject(['is_default_page'])
            if old_page is not None:
                for tr in old_page.getTranslations(review_state=False).values():
                    tr.reindexObject(['is_default_page'])

InitializeClass(I18NBaseObject)
