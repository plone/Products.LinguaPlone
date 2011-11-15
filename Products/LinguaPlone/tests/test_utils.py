import unittest

from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.utils import linkTranslations
from Products.LinguaPlone.utils import isInitialTranslationId


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


class InitialTranslationId(unittest.TestCase):

    def testInitialId(self):
        self.assertTrue(
            isInitialTranslationId('doc', 'doc', 'fr'))

    def testInitialIdInSameFolder(self):
        self.assertTrue(
            isInitialTranslationId('doc-fr', 'doc', 'fr'))

    def testCustomizedId(self):
        self.assertFalse(
            isInitialTranslationId('a-propos-de-la-langue',
                'about-language', 'fr'))

    def testStartWithCanonicalId(self):
        self.assertFalse(
            isInitialTranslationId('doc-en-francais', 'doc', 'fr'))
