#
# Folder Related Tests
#

from Products.LinguaPlone.tests import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation

import transaction

class TestFolderTranslation(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.folder_en = makeContent(self.folder, 'SimpleFolder', 'folder')
        self.folder_en.setLanguage('en')

    def testTranslationKeepSameIdInDifferentFolders(self):
        self.folder_de = makeTranslation(self.folder_en, 'de')
        english = makeContent(self.folder_en, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        self.assertEqual(english.getId(), german.getId())

    def testTranslationIsMovedToTranslatedFolder(self):
        self.folder_de = makeTranslation(self.folder_en, 'de')
        english = makeContent(self.folder_en, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        self.failUnless(english in self.folder_en.objectValues())
        self.failUnless(german in self.folder_de.objectValues())

    def testFolderTranslationMoveTranslatedContent(self):
        english1 = makeContent(self.folder_en, 'SimpleType', 'doc1')
        english1.setLanguage('en')
        english2 = makeContent(self.folder_en, 'SimpleType', 'doc2')
        english2.setLanguage('en')
        german1 = makeTranslation(english1, 'de')
        german2 = makeTranslation(english2, 'de')
        transaction.savepoint(optimistic=True)
        self.folder_de = makeTranslation(self.folder_en, 'de')
        self.failUnless(english1.getId() in self.folder_en.objectIds())
        self.failUnless(english2.getId() in self.folder_en.objectIds())
        self.failIf(english1.getId() in self.folder_de.objectIds())
        self.failIf(english2.getId() in self.folder_de.objectIds())
        self.failUnless(german1.getId() in self.folder_de.objectIds())
        self.failUnless(german2.getId() in self.folder_de.objectIds())
        self.failIf(german1.getId() in self.folder_en.objectIds())
        self.failIf(german2.getId() in self.folder_en.objectIds())

    def testSetLanguageMoveTranslatedContent(self):
        self.folder_de = makeTranslation(self.folder_en, 'de')
        en2de = makeContent(self.folder_en, 'SimpleType', 'doc2')
        en2de.setLanguage('en')
        transaction.savepoint(optimistic=True)
        en2de.setLanguage('de')
        self.failIf(en2de.getId() in self.folder_en.objectIds())
        self.failUnless(en2de.getId() in self.folder_de.objectIds())


class TestDynamicFolderProcessForm(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('pt')
        self.setLanguage('en')
        self.folder_en = makeContent(self.folder, 'DynamicFolder', 'folder')
        self.folder_en.setLanguage('en')
        self.english = makeContent(self.folder_en, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.folder_en.setDefaultPage(self.english.getId())
        self.portuguese = makeTranslation(self.english, 'pt')
        transaction.savepoint(optimistic=True)
        self.portuguese.processForm(values={'id' : 'foo', 'title' : 'Foo'})
        self.folder_pt = self.folder_en.getTranslation('pt')

    def testCreatedNewFolder(self):
        self.failIfEqual(self.folder_en, self.folder_pt)

    def testSetObjectId(self):
        self.assertEqual(self.portuguese.getId(), 'foo')

    def testSetObjectTitle(self):
        self.assertEqual(self.portuguese.Title(), 'Foo')

    def testChangedFolderId(self):
        self.assertEqual(self.folder_pt.getId(), 'folder-pt')

    def testChangedFolderTitle(self):
        self.assertEqual(self.folder_pt.Title(), 'Foo')

    def testMovedContentFromEnglish(self):
        self.failIf('doc-pt' in self.folder_en.objectIds())
        self.failIf('foo' in self.folder_en.objectIds())

    def testMovedAndRenamedContentIntoPortuguese(self):
        self.failUnless('foo' in self.folder_pt.objectIds())

    def testSetPageDefault(self):
        self.assertEqual(self.folder_pt.getDefaultPage(), 'foo')


class TestOrderedFolder(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.folder_en = makeContent(self.folder, 'OrderedFolder', 'folder')
        self.folder_en.setLanguage('en')

    def testNonZero(self):
        self.assertEqual(bool(self.folder_en), True)

    def testDelete(self):
        folder2 = makeContent(self.folder, 'OrderedFolder', 'folder2')
        folder2.setLanguage('en')
        del self.folder['folder2']
        self.failIf('folder2' in self.folder.keys())


class TestBTreeFolder(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.folder_en = makeContent(self.folder, 'BTreeFolder', 'folder')
        self.folder_en.setLanguage('en')

    def testNonZero(self):
        self.assertEqual(bool(self.folder_en), True)

    def testDelete(self):
        folder2 = makeContent(self.folder, 'BTreeFolder', 'folder2')
        folder2.setLanguage('en')
        del self.folder['folder2']
        self.failIf('folder2' in self.folder.keys())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFolderTranslation))
    suite.addTest(makeSuite(TestDynamicFolderProcessForm))
    suite.addTest(makeSuite(TestOrderedFolder))
    suite.addTest(makeSuite(TestBTreeFolder))
    return suite
