#
# Delete Tests
#

from Products.LinguaPlone.tests import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation

from Products.LinguaPlone import config
from OFS.ObjectManager import BeforeDeleteException


class TestDeleteTranslations(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')

    def testDeleteTranslationClearsReference(self):
        # Deleting a translation object should remove
        # the relation in the canonical object.
        german = makeTranslation(self.english, 'de')
        self.assertEqual(len(self.english.getTranslations()), 2)
        self.folder._delObject(german.getId())
        self.assertEqual(len(self.english.getTranslations()), 1)

    def testDeleteCanonical(self):
        # Deletion should be possible if there are no translations
        self.folder._delObject('doc')


class TestCanonicalProtection(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')

    def testDeleteCanonicalWithTranslations(self):
        # Must delete translations first
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        makeTranslation(english, 'de')
        self.assertRaises(BeforeDeleteException,
                          self.folder._delObject, 'doc')

    def testDeleteCanonicalWithTranslationsFolder(self):
        # Must delete translations first
        english = makeContent(self.folder, 'SimpleFolder', 'foo')
        english.setLanguage('en')
        makeTranslation(english, 'de')
        self.assertRaises(BeforeDeleteException,
                          self.folder._delObject, 'foo')

    def testDeleteCanonicalWithTranslationsOrderedFolder(self):
        # Must delete translations first
        english = makeContent(self.folder, 'OrderedFolder', 'foo')
        english.setLanguage('en')
        makeTranslation(english, 'de')
        self.assertRaises(BeforeDeleteException,
                          self.folder._delObject, 'foo')

    def testDeleteCanonicalWithTranslationsBTreeFolder(self):
        # Must delete translations first
        english = makeContent(self.folder, 'BTreeFolder', 'foo')
        english.setLanguage('en')
        makeTranslation(english, 'de')
        self.assertRaises(BeforeDeleteException,
                          self.folder._delObject, 'foo')

    def testBulkDeleteCanonical(self):
        # Should be able to delete if translations are deleted as well
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        self.folder.manage_delObjects(['doc', german.getId()])

    # XXX: Fails :-(
    def DISABLED_testBulkDeleteCanonicalReverseOrder(self):
        # Should be able to delete if translations are deleted as well
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        self.folder.manage_delObjects([german.getId(), 'doc'])

    # XXX: Fails :-(
    def DISABLED_testBulkDeleteCanonicalParentFolder(self):
        # Should be able to delete the parent folder
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        self.folder.Members.manage_delObjects(self.folder.getId())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDeleteTranslations))
    if config.CANONICAL_DELETE_PROTECTION:
        suite.addTest(makeSuite(TestCanonicalProtection))
    return suite
