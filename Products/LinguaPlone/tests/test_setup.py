import logging

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.tests.base import LinguaPloneTestCase


class Extra(object):

    fallback = False


class Context(object):

    def __init__(self, site):
        self.site = site

    def readDataFile(self, name):
        return True

    def getSite(self):
        return self.site

    def getLogger(self, name):
        return logging.getLogger(name)


class TestInstallSetup(LinguaPloneTestCase):

    def test_catalog_patch(self):
        from Products.CMFPlone.CatalogTool import CatalogTool
        from .. import config
        from .. import patches
        self.assert_('I18nAwareCatalog' in patches._enabled)
        if config.I18NAWARE_CATALOG:
            self.failUnless(hasattr(CatalogTool, '__lp_old_searchResults'))
        else:
            self.failIf(hasattr(CatalogTool, '__lp_old_searchResults'))
        # We can safely apply the patches again
        patches.I18nAwareCatalog()
        self.assert_('I18nAwareCatalog' in patches._enabled)

    def test_tools(self):
        portal = aq_base(self.portal)
        self.failUnless(hasattr(portal, 'archetype_tool'))
        self.failUnless(hasattr(portal, 'portal_languages'))

    def test_portal_types(self):
        types = aq_base(getToolByName(self.portal, 'portal_types'))
        self.failUnless(hasattr(types, 'SimpleType'))
        self.failUnless(hasattr(types, 'DerivedType'))
        self.failUnless(hasattr(types, 'SimpleFolder'))

    def test_language_index(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.assert_('Language' in catalog.indexes())
        index = catalog._catalog.getIndex('Language')
        self.assertEquals(index.meta_type, 'FieldIndex')
        self.assert_(index.numObjects() > 0)

    def test_language_index_replacement(self):
        from ..setuphandlers import importReindexLanguageIndex
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.assert_('Language' in catalog.indexes())
        catalog.delIndex('Language')
        catalog.addIndex('Language', 'LanguageIndex', Extra)
        self.assert_('Language' in catalog.indexes())
        index = catalog._catalog.getIndex('Language')
        self.assertEquals(index.meta_type, 'LanguageIndex')

        context = Context(self.portal)
        importReindexLanguageIndex(context)

        self.assert_('Language' in catalog.indexes())
        index = catalog._catalog.getIndex('Language')
        self.assertEquals(index.meta_type, 'FieldIndex')
        self.assert_(index.numObjects() > 0)
