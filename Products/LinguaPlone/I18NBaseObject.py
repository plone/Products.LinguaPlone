from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Acquisition import Implicit
from Acquisition import aq_inner
from Acquisition import aq_parent
from OFS.ObjectManager import BeforeDeleteException

from zope.interface import implements
from zope.event import notify

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DynamicType import DynamicType

from Products.Archetypes.atapi import BaseObject
from Products.Archetypes.utils import shasattr
from Products.Archetypes.config import LANGUAGE_DEFAULT
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.Archetypes.config import UID_CATALOG

from Products.LinguaPlone import events
from Products.LinguaPlone import config
from Products.LinguaPlone import permissions
from Products.LinguaPlone.interfaces import ILocateTranslation
from Products.LinguaPlone.interfaces import ITranslationFactory
from Products.LinguaPlone.interfaces import ITranslatable
from Products.CMFDynamicViewFTI.interface import ISelectableBrowserDefault


class AlreadyTranslated(Exception):
    """Raised when trying to create an existing translation."""
    pass


class TypeInfoWrapper:
    """Wrapper around typeinfo, used for the override of getTypeInfo
    used to intercept the edit alias and display translation form"""
    security = ClassSecurityInfo()

    def __init__(self, typeinfo):
        self.__typeinfo = typeinfo

    def __nonzero__(self):
        return bool(self.__typeinfo)


    security.declarePublic('getActionInfo')
    def getActionInfo(self, action_chain, object=None, check_visibility=0,
            check_condition=0):
        res = self.__typeinfo.getActionInfo(action_chain, object,
                check_visibility, check_condition)
        if action_chain=='object/edit':
            urlparts=res['url'].split('/')
            if urlparts[-1] in [ ('atct_edit', 'base_edit') ]:
                urlparts[-1]='translate_item'
                res['url']='/'.join(urlparts)

        return res


    security.declarePublic('queryMethodID')
    def queryMethodID(self, alias, default=None, context=None):
        if alias == 'edit':
            res = self.__typeinfo.queryMethodID(alias, default, context)
            if res in ('atct_edit', 'base_edit'):
                return 'translate_item'
        return self.__typeinfo.queryMethodID(alias, default, context)

    def __getattr__(self, value):
        return getattr(self.__typeinfo, value)


class I18NBaseObject(Implicit):
    """Base class for translatable objects."""
    implements(ITranslatable)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'isTranslation')
    def isTranslation(self):
        """Tells whether this object is used in a i18n context."""
        return bool(self.getReferenceImpl(config.RELATIONSHIP) or \
                    self.getBackReferenceImpl(config.RELATIONSHIP) \
                    and self.Language() or False)

    security.declareProtected(permissions.AddPortalContent, 'addTranslation')
    def addTranslation(self, language, *args, **kwargs):
        """Adds a translation."""
        if self.hasTranslation(language):
            translation = self.getTranslation(language)
            raise AlreadyTranslated, translation.absolute_url()

        locator = ILocateTranslation(self)
        parent = locator.findLocationForTranslation(language)

        notify(events.ObjectWillBeTranslatedEvent(self, language))

        canonical = self.getCanonical()
        kwargs[config.KWARGS_TRANSLATION_KEY] = canonical

        factory = ITranslationFactory(self)
        translation = factory.createTranslation(parent, language, *args, **kwargs)
        translation.reindexObject()
        notify(events.ObjectTranslatedEvent(self, translation, language))

        return translation


    security.declareProtected(permissions.AddPortalContent,
                              'addTranslationReference')
    def addTranslationReference(self, translation):
        """Adds the reference used to keep track of translations."""
        if self.hasTranslation(translation.Language()):
            double = self.getTranslation(translation.Language())
            raise AlreadyTranslated, double.absolute_url()
        self.addReference(translation, config.RELATIONSHIP)

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
        translation.deleteReference(self, config.RELATIONSHIP)

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
    def getTranslations(self):
        """Returns a dict of {lang : [object, wf_state]}, pass on to layer."""
        if self.isCanonical():
            result = {}
            workflow_tool = getToolByName(self, 'portal_workflow', None)
            if workflow_tool is None:
                # No context, most likely FTP or WebDAV
                result[self.Language()] = [self, None]
                return result
            lang = self.Language()
            state = workflow_tool.getInfoFor(self, 'review_state', None)
            result[lang] = [self, state]
            for obj in self.getTranslationBackReferences(objects=True):
                if obj is None:
                    continue
                lang = obj.Language()
                state = workflow_tool.getInfoFor(obj, 'review_state', None)
                result[lang] = [obj, state]
            return result
        else:
            return self.getCanonical().getTranslations()

    security.declareProtected(permissions.View, 'getNonCanonicalTranslations')
    def getNonCanonicalTranslations(self):
        """Returns a dict of {lang : [object, wf_state]}."""
        translations = self.getTranslations()
        non_canonical = {}
        for lang in translations.keys():
            if not translations[lang][0].isCanonical():
                non_canonical[lang] = translations[lang]
        return non_canonical

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
            translations = self.getTranslations()
            for obj, wfstate in translations.values():
                obj.deleteReferences(config.RELATIONSHIP)
            for obj, wfstate in translations.values():
                if obj != self:
                    obj.addTranslationReference(self)

    security.declareProtected(permissions.View, 'getCanonicalLanguage')
    def getCanonicalLanguage(self):
        """Returns the language code for the canonical language."""
        return self.getCanonical().Language()

    security.declareProtected(permissions.View, 'getCanonical')
    def getCanonical(self):
        """Returns the canonical translation."""
        ret = None
        if self.isCanonical():
            ret = self
        else:
            refs = self.getTranslationReferences()
            if refs:
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
                raise AlreadyTranslated, translation.absolute_url()
        self.getField('language').set(self, value, **kwargs)

        if not value:
            self.deleteReferences(config.RELATIONSHIP)

        parent = aq_parent(aq_inner(self))

        locator = ILocateTranslation(self)
        new_parent = locator.findLocationForTranslation(value)

        if new_parent != parent:
            info = parent.manage_cutObjects([self.getId()])
            new_parent.manage_pasteObjects(info)
        self.reindexObject()
        self._catalogRefs(self)

    security.declarePrivate('defaultLanguage')
    def defaultLanguage(self):
        """Returns the initial default language."""
        parent = aq_parent(aq_inner(self))
        if getattr(parent, 'portal_type', None) == 'TempFolder':# We have factory tool
            parent = aq_parent(aq_parent(parent))
        if ITranslatable.providedBy(parent):
            language = parent.Language()
            if language:
                return parent.Language()

        language_tool = getToolByName(self, 'portal_languages', None)
        if language_tool:
            if language_tool.startNeutral():
                return ''
            else:
                return language_tool.getPreferredLanguage()
        else:
            return LANGUAGE_DEFAULT

    security.declareProtected(permissions.ModifyPortalContent, 'processForm')
    def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
        """Process the schema looking for data in the form."""
        is_new_object = self.checkCreationFlag()
        
        BaseObject.processForm(self, data, metadata, REQUEST, values)
        if config.AUTO_NOTIFY_CANONICAL_UPDATE:
            if self.isCanonical():
                self.invalidateTranslations()

        if self._at_rename_after_creation and is_new_object:
            new_id = self._renameAfterCreation()

        if shasattr(self, '_lp_default_page'):
            delattr(self, '_lp_default_page')
            language = self.Language()
            canonical = self.getCanonical()
            parent = aq_parent(aq_inner(self))
            if ITranslatable.providedBy(parent):
                if not parent.hasTranslation(language):
                    parent.addTranslation(language)
                    translation_parent = parent.getTranslation(language)
                    translation_parent.processForm(
                            values=dict(title=self.Title()))
                    translation_parent.setDescription(self.Description())
                    parent = translation_parent

                if ISelectableBrowserDefault.providedBy(parent):
                    parent.setDefaultPage(new_id)

            
        if shasattr(self, '_lp_outdated'):
            delattr(self, '_lp_outdated')

    security.declareProtected(permissions.ModifyPortalContent, 'invalidateTranslations')
    def invalidateTranslations(self):
        """Outdates all translations except the canonical one."""
        translations = self.getNonCanonicalTranslations()
        for lang in translations.keys():
            translations[lang][0].notifyCanonicalUpdate()

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
            if self.isCanonical() and self.getNonCanonicalTranslations():
                raise BeforeDeleteException, 'Please delete translations first.'

    # Wrapper around typeinfo to hook into the edit alias
    security.declareProtected(permissions.AccessContentsInformation, 'getTypeInfo')
    def getTypeInfo(self):
        """Get the TypeInformation object specified by the portal type,
        possibly wrapped to intercept the edit alias.
        """
        ti = DynamicType.getTypeInfo(self)
        if ti is not None and not self.isCanonical():
            return TypeInfoWrapper(ti)
        return ti

    security.declareProtected(permissions.View, 'getTranslationReferences')
    def getTranslationReferences(self, objects=False):
        """Get all translation references for this object"""
        sID = self.UID()
        tool = getToolByName(self, REFERENCE_CATALOG)
        brains = tool._queryFor(sid=sID, relationship=config.RELATIONSHIP)
        if brains:
            if objects:
                return [
                    self._getReferenceObject(brain.targetUID)
                    for brain in brains
                ]
            else:
                return brains
        return []

    security.declareProtected(permissions.View, 'getTranslationBackReferences')
    def getTranslationBackReferences(self, objects=False):
        """Get all translation back references for this object"""
        tID = self.UID()
        tool = getToolByName(self, REFERENCE_CATALOG)
        brains = tool._queryFor(tid=tID, relationship=config.RELATIONSHIP)
        if brains:
            if objects:
                return [
                    self._getReferenceObject(brain.sourceUID)
                    for brain in brains
                ]
            else:
                return brains
        return []

    def _getReferenceObject(self, uid):
        tool = getToolByName(self, UID_CATALOG, None)
        brains = tool(UID=uid)
        for brain in brains:
            obj = brain.getObject()
            if obj is not None:
                return obj
        return None


InitializeClass(I18NBaseObject)
