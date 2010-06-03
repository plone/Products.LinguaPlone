#
# Setup Tests
#

from Products.LinguaPlone.tests import LinguaPloneTestCase

from Products.CMFPlone.CatalogTool import CatalogTool
from Products.LinguaPlone import config

from Acquisition import aq_base


class TestPatchesSetup(LinguaPloneTestCase.LinguaPloneTestCase):

    def testCatalogPatch(self):
        if config.I18NAWARE_CATALOG:
            self.failUnless(hasattr(CatalogTool, '__lp_old_searchResults'))
        else:
            self.failIf(hasattr(CatalogTool, '__lp_old_searchResults'))


class TestInstallSetup(LinguaPloneTestCase.LinguaPloneTestCase):

    def testTools(self):
        # Check all tools are installed
        portal = aq_base(self.portal)
        self.failUnless(hasattr(portal, 'archetype_tool'))
        self.failUnless(hasattr(portal, 'portal_languages'))

    def testPortalTypes(self):
        # Check all content types are installed
        types = aq_base(self.portal.portal_types)
        self.failUnless(hasattr(types, 'Lingua Item'))
        self.failUnless(hasattr(types, 'Lingua Folder'))
        # Dummies
        self.failUnless(hasattr(types, 'SimpleType'))
        self.failUnless(hasattr(types, 'DerivedType'))
        self.failUnless(hasattr(types, 'SimpleFolder'))

    def testExampleTypes(self):
        self.folder.invokeFactory('Lingua Item', id='foo')
        self.failUnless('foo' in self.folder.objectIds())
        self.folder.invokeFactory('Lingua Folder', id='bar')
        self.failUnless('bar' in self.folder.objectIds())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPatchesSetup))
    suite.addTest(makeSuite(TestInstallSetup))
    return suite
