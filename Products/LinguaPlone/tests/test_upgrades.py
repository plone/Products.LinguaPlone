from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.tests.base import LinguaPloneTestCase


class TestUpgrades(LinguaPloneTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addLanguage('de')
        self.addLanguage('no')

    def test_add_language_metadata(self):
        from ..migrations import add_language_metadata
        tool = getToolByName(self.portal, 'reference_catalog')
        tool.delColumn('Language')
        self.assert_('Language' not in tool.schema())
        for i in range(2):
            add_language_metadata(self.portal)
        self.assert_('Language' in tool.schema())

    def test_add_uid_language_index(self):
        from ..migrations import add_uid_language_index
        tool = getToolByName(self.portal, 'uid_catalog')
        tool.delIndex('Language')
        self.assert_('Language' not in tool.indexes())
        for i in range(2):
            add_uid_language_index(self.portal)
        self.assert_('Language' in tool.indexes())
        index = tool._catalog.getIndex('Language')
        self.assert_(index.numObjects() > 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUpgrades))
    return suite
