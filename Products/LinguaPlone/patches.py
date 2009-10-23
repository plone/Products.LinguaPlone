from Products.LinguaPlone.config import I18NAWARE_CATALOG
from Products.LinguaPlone.config import NOFILTERKEYS

_enabled = []

def AlreadyApplied(patch):
    if patch in _enabled:
        return True
    _enabled.append(patch)
    return False


# Patches the catalog tool to filter languages
def I18nAwareCatalog():
    if AlreadyApplied('I18nAwareCatalog'):
        return

    try:
        from App.special_dtml import DTMLFile
    except ImportError:
        from Globals import DTMLFile

    from Products.CMFPlone.CatalogTool import CatalogTool
    from Products.CMFCore.utils import getToolByName

    def searchResults(self, REQUEST=None, **kw):
        """ Calls ZCatalog.searchResults with extra arguments that
            limit the results to what the user is allowed to see.

            This version only returns the results for the current
            language, unless you explicitly ask for all results by
            providing the Language="all" keyword.
        """
        kw = kw.copy()
        languageTool = getToolByName(self, 'portal_languages', None)

        # When searching on certain indexes we don't want language filtering.
        def filterSearch(query, nofilter=NOFILTERKEYS):
            if not query:
                return 1
            for key in nofilter:
                if key in query:
                    return 0
            return 1

        if languageTool is not None and filterSearch(REQUEST) and filterSearch(kw):
            try:
                kw['Language'] = [languageTool.getPreferredLanguage(), '']
            except AttributeError:
                pass
        # 'all' deletes the query key
        elif REQUEST and REQUEST.get('Language', '') == 'all':
            del REQUEST['Language']
        elif kw.get('Language', '') == 'all':
            del kw['Language']

        return self.__lp_old_searchResults(REQUEST, **kw)

    CatalogTool.__lp_old_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults
    CatalogTool.manage_catalogView = DTMLFile('www/catalogView',globals())


if I18NAWARE_CATALOG:
    I18nAwareCatalog()


# Make sure the addSupportedLanguage method works without checking the
# vocabularies
from Products.PloneLanguageTool import LanguageTool

def new_addSupportedLanguage(self, langCode):
    """Registers a language code as supported."""
    value = str(langCode)
    languages = [str(l) for l in self.supported_langs]
    if value not in languages:
        languages.append(value)
    self.supported_langs = languages

LanguageTool.addSupportedLanguage = new_addSupportedLanguage
