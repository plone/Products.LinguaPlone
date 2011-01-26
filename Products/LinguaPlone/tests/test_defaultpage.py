from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestFolderDefaultPage(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')

    def testOriginalBehavior(self):
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, None)

    def testEnglishAsDefault(self):
        self.folder.setDefaultPage(self.english.getId())
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, self.english.getId())

    def testGermanAsDefault(self):
        self.setLanguage('de')
        self.folder.setDefaultPage(self.english.getId())
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, self.english.getId())

    def testInvalidAsDefault(self):
        self.folder.setDefaultPage('pt')
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, None)


class TestSimpleFolderBrowserDefault(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.folder_en = makeContent(self.folder, 'SimpleFolder', 'folder_en')
        self.folder_en.setLanguage('en')

    def testBrowserDefault(self):
        obj, views = self.folder_en.__browser_default__(None)
        self.assertEqual(obj, self.folder_en)
        self.assertEqual(views, ['base_view'])


class TestPortalDefaultPage(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.setRoles(['Manager'])
        self.english = makeContent(self.portal, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')

    def testOriginalBehavior(self):
        result = self.portal.getDefaultPage()
        self.failUnlessEqual(result, 'front-page')

    def testEnglishAsDefault(self):
        self.portal.setDefaultPage(self.english.getId())
        result = self.portal.getDefaultPage()
        self.failUnlessEqual(result, self.english.getId())

    def testGermanAsDefault(self):
        self.setLanguage('de')
        self.portal.setDefaultPage(self.english.getId())
        result = self.portal.getDefaultPage()
        self.failUnlessEqual(result, self.english.getId())

    def testInvalidAsDefault(self):
        self.folder.setDefaultPage('pt')
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, None)


class TestIndexDefaultPage(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'index_html')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')

    def testOriginalBehavior(self):
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, self.english.getId())

    def testEnglishAsDefault(self):
        self.folder.setDefaultPage(self.english.getId())
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, self.english.getId())

    def testGermanAsDefault(self):
        self.setLanguage('de')
        self.folder.setDefaultPage(self.english.getId())
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, self.english.getId())

    def testInvalidAsDefault(self):
        self.folder.setDefaultPage('pt')
        result = self.folder.getDefaultPage()
        self.failUnlessEqual(result, 'index_html')


class DefaultPageTranslationTests(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.setRoles(['Manager'])

    def testTranslatingDefaultPageCreatesTranslatedParentFolder(self):
        english_folder = self.folder
        english_doc = makeContent(english_folder, 'SimpleType', 'doc')
        english_folder.setDefaultPage(english_doc.getId())
        makeTranslation(english_doc, 'de').processForm(
            values=dict(title='dok'))
        german_folder = english_folder.getTranslation('de')
        german_doc = english_doc.getTranslation('de')
        self.assertNotEqual(english_folder, german_folder)
        self.assertTrue(german_doc in german_folder.objectValues())

    def testTranslatingDefaultPagePutsItIntoTranslatedParentFolder(self):
        english_folder = self.folder
        makeTranslation(english_folder, 'de')   # translated folder exists
        english_doc = makeContent(english_folder, 'SimpleType', 'doc')
        english_folder.setDefaultPage(english_doc.getId())
        makeTranslation(english_doc, 'de').processForm(
            values=dict(title='dok'))
        german_folder = english_folder.getTranslation('de')
        german_doc = english_doc.getTranslation('de')
        self.assertTrue(german_doc in german_folder.objectValues())


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
