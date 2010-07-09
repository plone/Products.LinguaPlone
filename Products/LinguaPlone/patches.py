from Products.LinguaPlone.config import I18NAWARE_CATALOG
from Products.LinguaPlone.catalog import languageFilter

_enabled = []


def AlreadyApplied(patch):
    if patch in _enabled:
        return True
    _enabled.append(patch)
    return False


def I18nAwareCatalog():
    # Patches the catalog tool to filter languages
    if AlreadyApplied('I18nAwareCatalog'):
        return

    from App.special_dtml import DTMLFile
    from Products.CMFPlone.CatalogTool import CatalogTool

    def searchResults(self, REQUEST=None, **kw):
        """ Calls ZCatalog.searchResults with extra arguments that
            limit the results to what the user is allowed to see.

            This version only returns the results for the current
            language, unless you explicitly ask for all results by
            providing the Language="all" keyword.
        """
        if REQUEST is not None and kw.get('Language', '') != 'all':
            languageFilter(REQUEST)
        else:
            languageFilter(kw)
        return self.__lp_old_searchResults(REQUEST, **kw)

    CatalogTool.__lp_old_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults
    CatalogTool.manage_catalogView = DTMLFile('www/catalogView', globals())


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
