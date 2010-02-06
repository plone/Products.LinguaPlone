from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.interface import alsoProvides

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView


class SetupView(BrowserView):

    fixDefaultPage = False

    def __call__(self, forceOneLanguage=False):
        result = []
        self.folders = {}
        pl = getToolByName(self.context, "portal_languages")
        self.languages = languages = pl.getSupportedLanguages()
        if len(languages) == 1 and not forceOneLanguage:
            raise Exception('Only one supported language configured.')
        self.defaultLanguage = pl.getDefaultLanguage()
        for language in languages:
            result.extend(self.setUpLanguage(language,
                pl.getNameForLanguageCode(language)))
        result.extend(self.linkTranslations())
        result.extend(self.removePortalDefaultPage())
        if self.fixDefaultPage:
            result.extend(self.resetDefaultPage())
        if not result:
            return "Nothing done"
        else:
            result.insert(0, "Setup of language root folders on Plone site "
                "'%s'" % self.context.getId())
            return '\n'.join(result)

    def linkTranslations(self):
        result = []
        doneSomething = False
        canonical = self.folders[self.defaultLanguage]
        for language in self.languages:
            if ((language <> self.defaultLanguage) and (not
                canonical.hasTranslation(language))):
                self.folders[language].addTranslationReference(canonical)
                doneSomething = True
        if doneSomething:
            result.append("Translations linked.")
        return result

    def setUpLanguage(self, code, name):
        result = []
        folderId = "%s" % code
        folder = getattr(self.context, folderId, None)
        if folder is None:
            self.context.invokeFactory('Folder', folderId)
            folder = getattr(self.context, folderId)
            folder.setLanguage(code)
            folder.setTitle(name)
            folder.reindexObject()
            result.append("Added '%s' folder: %s" % (code, folderId))
        self.folders[code] = folder
        if not INavigationRoot.providedBy(folder):
            alsoProvides(folder, INavigationRoot)
            result.append("INavigationRoot setup on folder '%s'" % code )
        return result

    def removePortalDefaultPage(self):
        result = []
        defaultPageId = self.context.getDefaultPage()
        if not defaultPageId:
            return result
        self.previousDefaultPage = getattr(self.context, defaultPageId)
        self.context.setDefaultPage(None)
        self.fixDefaultPage = True
        result.append('Portal default page removed.')
        return result

    def resetDefaultPage(self):
        result = []
        language = self.previousDefaultPage.Language()
        pageId = self.previousDefaultPage.getId()
        # test language neutral
        if language == '':
            language = self.defaultLanguage
        if language not in self.languages:
            result.append("WARNING : Default page '%s' is of language '%s' "
                "which is not available !" % (pageId, language))
        else:
            target = self.folders[language]
            objects = self.context.manage_cutObjects(pageId)
            target.manage_pasteObjects(objects)
            target.setDefaultPage(pageId)
            target.reindexObject()
            defaultPage = getattr(target, pageId)
            defaultPage.reindexObject()
            result.append("Moved default page '%s' to folder '%s'" %
                (pageId, target.getId()))
        return result
