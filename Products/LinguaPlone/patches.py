from Products.LinguaPlone.config import I18NAWARE_CATALOG
from Products.LinguaPlone.config import NOFILTERKEYS

_enabled = []

def AlreadyApplied(patch):
    if patch in _enabled:
        return True
    _enabled.append(patch)
    return False


# PATCH 2
#
# Patches the catalog tool to filter languages
#
def I18nAwareCatalog():
    if AlreadyApplied('I18nAwareCatalog'):
        return

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


# PATCH 3
#
# Patches kupu to allow a single portal type to be used as a resource
# type
#
def PortalTypeAsResourceType():
    if AlreadyApplied('PortalTypeAsResourceType'):
        return

    import Products.kupu.plone.plonedrawers

    PREFIX = 'linguaplone-'
    BaseResourceType = Products.kupu.plone.plonedrawers.ResourceType
    class LinguaPloneResourceType(BaseResourceType):
        def __init__(self, tool, name):
            if name.startswith(PREFIX):
                self.name = name
                self._tool = tool
                self._portal_types = name[len(PREFIX):].split(',')
                self._field = self._widget = None
            else:
                BaseResourceType.__init__(self, tool, name)

    Products.kupu.plone.plonedrawers.ResourceType = LinguaPloneResourceType

if I18NAWARE_CATALOG:
    I18nAwareCatalog()

PortalTypeAsResourceType()
