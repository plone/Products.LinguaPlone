from Products.LinguaPlone.tests.LinguaPloneTestCase import LinguaPloneTestCase
from Products.LinguaPlone.utils import linkTranslations

class TestContentLinker(LinguaPloneTestCase):
    def afterSetUp(self):
        self.addLanguage("en")
        self.addLanguage("nl")
        self.folder.invokeFactory("SimpleType", "frontpage")
        self.folder.invokeFactory("SimpleType", "voorpagina")
        self.folder.invokeFactory("SimpleFolder", "images")
        self.folder.images.invokeFactory("SimpleType", "logo")
        self.folder.invokeFactory("SimpleFolder", "plaatjes")
        self.folder.plaatjes.invokeFactory("SimpleType", "logo")

    def testSameFolderLinking(self):
        todo=[[(["frontpage"], "en"), (["voorpagina"], "nl")]]
        linkTranslations(self.folder, todo)
        self.assertEqual(self.folder.frontpage.getLanguage(), "en")
        self.assertEqual(self.folder.voorpagina.getLanguage(), "nl")
        self.assertEqual(self.folder.frontpage.isTranslation(), True)
        self.assertEqual(self.folder.voorpagina.isTranslation(), True)
        self.assertEqual(self.folder.voorpagina.getTranslation("en"),
                self.folder.frontpage)
        self.assertEqual(self.folder.frontpage.getTranslation("nl"),
                self.folder.voorpagina)
        self.assertEqual(self.folder.frontpage.isCanonical(), True)
    

    def testSubFolderLinking(self):
        todo=[[(["images", "logo"], "en"), (["plaatjes", "logo"], "nl")]]
        linkTranslations(self.folder, todo)
        self.assertEqual(self.folder.images.logo.getLanguage(), "en")
        self.assertEqual(self.folder.plaatjes.logo.getLanguage(), "nl")
        self.assertEqual(self.folder.images.logo.getTranslation("nl"),
                self.folder.plaatjes.logo)
        self.assertEqual(self.folder.plaatjes.logo.getTranslation("en"),
                self.folder.images.logo)
        self.assertEqual(self.folder.images.logo.isCanonical(), True)


    def testTypeMismatch(self):
        todo=[[(["frontpage"], "en"), (["images"], "nl")]]
        self.assertRaises(ValueError, linkTranslations, self.folder, todo)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestContentLinker))
    return suite


