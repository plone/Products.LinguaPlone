# Plone Solutions AS <info@plonesolutions.com>
# http://www.plonesolutions.com

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

"""
Baseclass for multilingual content.
"""


from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Acquisition import Implicit
from Acquisition import aq_inner
from Acquisition import aq_parent
from OFS.ObjectManager import BeforeDeleteException

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DynamicType import DynamicType

from Products.Archetypes.public import *
from Products.Archetypes.utils import shasattr
from Products.Archetypes.config import LANGUAGE_DEFAULT

from Products.LinguaPlone import events
from Products.LinguaPlone import config
from Products.LinguaPlone import permissions

from zope.interface import implements
from zope.event import notify
from Products.LinguaPlone.interfaces import ITranslatable

from Products.CMFDynamicViewFTI.interface import ISelectableBrowserDefault

from plone.locking.interfaces import ILockable

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.utils import isDefaultPage
try:
    from Products.CMFPlone.interfaces.Translatable \
            import ITranslatable as Z2ITranslatable
except ImportError:
    # Forward-compatibility: this interface will disappear from CMFPlone
    Z2ITranslatable = (())


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
    __implements__ = (Z2ITranslatable,)
    implements(ITranslatable)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'isTranslation')
    def isTranslation(self):
        """Tells whether this object is used in a i18n context."""
        return bool(self.getReferenceImpl(config.RELATIONSHIP) or \
                    self.getBackReferenceImpl(config.RELATIONSHIP) \
                    and self.getLanguage() or False)

    security.declareProtected(permissions.AddPortalContent, 'addTranslation')
    def addTranslation(self, language, *args, **kwargs):
        """Adds a translation."""
        canonical = self.getCanonical()
        parent = aq_parent(aq_inner(self))
        if ITranslatable.providedBy(parent):
            parent = parent.getTranslation(language) or parent
        if self.hasTranslation(language):
            translation = self.getTranslation(language)
            raise AlreadyTranslated, translation.absolute_url()
        beforeevent = events.ObjectWillBeTranslatedEvent(self, language)
        notify(beforeevent)         
        id = canonical.getId()
        while not parent.checkIdAvailable(id):
            id = '%s-%s' % (id, language)
        kwargs[config.KWARGS_TRANSLATION_KEY] = canonical
        if kwargs.get('language', None) != language:
            kwargs['language'] = language
        o = _createObjectByType(self.portal_type, parent, id, *args, **kwargs)
        # If there is a custom factory method that doesn't add the
        # translation relationship, make sure it is done now.
        if o.getCanonical() != canonical:
            o.addTranslationReference(canonical)
        self.invalidateTranslationCache()        
        # Copy over the language independent fields
        schema = canonical.Schema()
        independent_fields = schema.filterFields(languageIndependent=True)
        for field in independent_fields:
            accessor = field.getEditAccessor(canonical)
            if not accessor:
                accessor = field.getAccessor(canonical)
            data = accessor()
            mutatorname = getattr(field, 'translation_mutator', None)
            if mutatorname is None:
                # seems we have some field from archetypes.schemaextender
                # or something else not using ClassGen
                # fall back to default mutator
                o.getField(field.getName()).set(self, data)
            else:
                # holy ClassGen crap - we have a generated method!
                translation_mutator = getattr(o, mutatorname)
                translation_mutator(data)
        # If this is a folder, move translated subobjects aswell.
        if self.isPrincipiaFolderish:
            moveids = []
            for obj in self.objectValues():
                if ITranslatable.providedBy(obj) and \
                           obj.getLanguage() == language:
                    lockable = ILockable(obj, None)
                    if lockable is not None and lockable.can_safely_unlock():
                        lockable.unlock()
                    moveids.append(obj.getId())
            if moveids:
                o.manage_pasteObjects(self.manage_cutObjects(moveids))
        o.reindexObject()
        if isDefaultPage(canonical, self.REQUEST):
            o._lp_default_page = True
        afterevent = events.ObjectTranslatedEvent(self, o, language)
        notify(afterevent)             

    security.declareProtected(permissions.AddPortalContent,
                              'addTranslationReference')
    def addTranslationReference(self, translation):
        """Adds the reference used to keep track of translations."""
        if self.hasTranslation(translation.Language()):
            double = self.getTranslation(translation.Language())
            raise AlreadyTranslated, double.absolute_url()
        if self.portal_type!=translation.portal_type:
            raise ValueError, "Can only link objects of the same portal type"
        self.addReference(translation, config.RELATIONSHIP)
        self.invalidateTranslationCache()

    security.declareProtected(permissions.ModifyPortalContent,
                              'removeTranslation')
    def removeTranslation(self, language):
        """Removes a translation, pass on to layer."""
        translation = self.getTranslation(language)
        if translation.isCanonical():
            self.setCanonical()
        translation_parent = aq_parent(aq_inner(translation))
        translation_parent.manage_delObjects([translation.getId()])
        self.invalidateTranslationCache()

    security.declareProtected(permissions.ModifyPortalContent,
                              'removeTranslationReference')
    def removeTranslationReference(self, translation):
        """Removes the translation reference."""
        translation.deleteReference(self, config.RELATIONSHIP)
        self.invalidateTranslationCache()

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
        l = self.getTranslations().get(language, None)
        return l and l[0] or l

    security.declareProtected(permissions.View, 'getTranslationLanguages')
    def getTranslationLanguages(self):
        """Returns a list of language codes.

        Note that we return all translations available. If you want only
        the translations from the current portal_language selected list,
        you should use the getTranslatedLanguages script.
        """
        return self.getTranslations().keys()

    security.declareProtected(permissions.View, 'getTranslations')
    def getTranslations(self):
        """Returns a dict of {lang : [object, wf_state]}, pass on to layer."""
        if self.isCanonical():
            if config.CACHE_TRANSLATIONS and \
               getattr(self, '_v_translations', None):
                return self._v_translations
            result = {}
            workflow_tool = getToolByName(self, 'portal_workflow', None)
            if workflow_tool is None:
                # No context, most likely FTP or WebDAV
                result[self.getLanguage()] = [self, None]
                return result
            lang = self.getLanguage()
            state = workflow_tool.getInfoFor(self, 'review_state', None)
            result[lang] = [self, state]
            for obj in self.getBRefs(config.RELATIONSHIP):
                lang = obj.getLanguage()
                state = workflow_tool.getInfoFor(obj, 'review_state', None)
                result[lang] = [obj, state]
            if config.CACHE_TRANSLATIONS:
                self._v_translations = result
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
        try:
            return not bool(self.getReferenceImpl(config.RELATIONSHIP))
        except AttributeError:
            return True

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
            self.invalidateTranslationCache()

    security.declareProtected(permissions.View, 'getCanonicalLanguage')
    def getCanonicalLanguage(self):
        """Returns the language code for the canonical language."""
        return self.getCanonical().getLanguage()

    security.declareProtected(permissions.View, 'getCanonical')
    def getCanonical(self):
        """Returns the canonical translation."""
        if config.CACHE_TRANSLATIONS and getattr(self, '_v_canonical', None):
            return self._v_canonical
        ret = None

        if self.isCanonical():
            ret = self
        else:
            refs = self.getRefs(config.RELATIONSHIP)
            ret = refs and refs[0] or None

        if config.CACHE_TRANSLATIONS:
            self._v_canonical = ret
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
        translation = self.getTranslation(value)
        if self.hasTranslation(value):
            if translation == self:
                return
            else:
                raise AlreadyTranslated, translation.absolute_url()
        self.getField('language').set(self, value, **kwargs)

        # If we are called during a schema update we should not be deleting
        # any language relations.
        req = getattr(self, 'REQUEST', None)
        if shasattr(req, 'get'):
            if req.get('SCHEMA_UPDATE', None) is not None:
                return

        if not value:
            self.deleteReferences(config.RELATIONSHIP)

        parent = aq_parent(aq_inner(self))
        if ITranslatable.providedBy(parent):
            new_parent = parent.getTranslation(value) or parent
            if new_parent != parent:
                info = parent.manage_cutObjects([self.getId()])
                new_parent.manage_pasteObjects(info)
        self.reindexObject()
        self.invalidateTranslationCache()

    security.declarePrivate('defaultLanguage')
    def defaultLanguage(self):
        """Returns the initial default language."""
        parent = aq_parent(aq_inner(self))
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
            language = self.getLanguage()
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
        self.invalidateTranslationCache()

    security.declarePrivate('invalidateTranslationCache')
    def invalidateTranslationCache(self):
        if config.CACHE_TRANSLATIONS:
            if shasattr(self, '_v_canonical'):
                delattr(self, '_v_canonical')
            if shasattr(self, '_v_translations'):
                delattr(self, '_v_translations')
            if not self.isCanonical():
                self.getCanonical().invalidateTranslationCache()

    security.declarePrivate('notifyCanonicalUpdate')
    def notifyCanonicalUpdate(self):
        """Marks the translation as outdated."""
        self._lp_outdated = True

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


InitializeClass(I18NBaseObject)
