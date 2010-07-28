from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.config import I18NAWARE_CATALOG
from Products.LinguaPlone.config import NOFILTERKEYS


def languageFilter(query):
    """ add preferred language to query parameters (in-place) """
    if not I18NAWARE_CATALOG:
        return
    site = getSite()
    languageTool = getToolByName(site, 'portal_languages', None)
    if languageTool is None:
        return
    if query.get('Language') == 'all':
        del query['Language']
        return
    for key in NOFILTERKEYS:    # any "nofilter" indexing prevent mangling
        if key in query:
            return
    query['Language'] = [languageTool.getPreferredLanguage(), '']
