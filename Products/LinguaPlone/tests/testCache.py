#
# Cache Tests
#

from Products.LinguaPlone.tests import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation

from Products.LinguaPlone import config


class TestCanonicalCache(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')

    def testCanonicalIsCached(self):
        canonical = getattr(self.english, '_v_canonical', None)
        self.assertEqual(canonical, None)
        self.english.getCanonical()
        canonical = getattr(self.english, '_v_canonical', None)
        self.assertEqual(canonical, self.english)

    def testInvalidatedOnCanonical(self):
        german = makeTranslation(self.english, 'de')
        german.setCanonical()
        canonical = getattr(german, '_v_canonical', None)
        self.assertEqual(canonical, None)

    def testInvalidatedOnNonCanonical(self):
        german = makeTranslation(self.english, 'de')
        german.setCanonical()
        canonical = getattr(self.english, '_v_canonical', None)
        self.assertEqual(canonical, None)

    def testUpdatedOnCanonical(self):
        german = makeTranslation(self.english, 'de')
        german.setCanonical()
        german.getCanonical()
        canonical = getattr(german, '_v_canonical', None)
        self.assertEqual(canonical, german)

    def testUpdatedOnNonCanonical(self):
        german = makeTranslation(self.english, 'de')
        german.setCanonical()
        self.english.getCanonical()
        canonical = getattr(self.english, '_v_canonical', None)
        self.assertEqual(canonical, german)


class TestTranslationsCache(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.bulgarian = makeContent(self.folder, 'SimpleType', 'doc1')
        self.bulgarian.setLanguage('bg')
        self.russian = makeContent(self.folder, 'SimpleType', 'doc2')
        self.russian.setLanguage('ru')

    def testTranslationsAreCached(self):
        translations = getattr(self.english, '_v_translations', None)
        self.assertEqual(len(translations), 1)
        german = makeTranslation(self.english, 'de')
        self.english.getTranslations()
        translations = getattr(self.english, '_v_translations', None)
        self.assertEqual(len(translations), 2)

    def testInvalidatedOnCanonicalObject(self):
        german = makeTranslation(self.english, 'de')
        self.english.getTranslations()
        self.english.invalidateTranslations()
        translations = getattr(self.english, '_v_translations', None)
        self.assertEqual(translations, None)

    def testInvalidatedOnNonCanonical(self):
        german = makeTranslation(self.english, 'de')
        german.getTranslations()
        german.invalidateTranslations()
        translations = getattr(german, '_v_translations', None)
        self.assertEqual(translations, None)

    def testUpdatedOnCanonical(self):
        german = makeTranslation(self.english, 'de')
        self.english.getTranslations()
        translations = getattr(self.english, '_v_translations', None)
        self.assertEqual(len(translations), 2)
        self.failUnless('de' in translations.keys())
        self.assertEqual(german, translations['de'][0])
        self.failUnless('en' in translations.keys())
        self.assertEqual(self.english, translations['en'][0])

    def testUpdatedOnNonCanonical(self):
        german = makeTranslation(self.english, 'de')
        german.getTranslations()
        translations = getattr(german, '_v_translations', None)
        self.assertEqual(len(translations), 1)
        self.failUnless('de' in translations.keys())
        self.assertEqual(german, translations['de'][0])

    def testSetLanguageInvalidate(self):
        self.addLanguage('fr')
        de2fr = makeTranslation(self.english, 'de')
        de2fr.setLanguage('fr')
        de2fr.getTranslations()
        translations = getattr(self.english, '_v_translations', None)
        self.assertEqual(len(translations), 2)
        self.failUnless('fr' in translations.keys())
        self.assertEqual(de2fr, translations['fr'][0])
        self.failUnless('en' in translations.keys())
        self.assertEqual(self.english, translations['en'][0])

    def testAddTranslationReference(self):
        self.english.addTranslationReference(self.bulgarian) # make it canonical
        self.english.getTranslations() # cache the translations
        self.english.addTranslationReference(self.russian)
        translations = self.english.getTranslations()
        self.assertEqual(len(translations), 3)

    def testRemoveTranslationReference(self):
        self.english.addTranslationReference(self.bulgarian) # make it canonical
        self.english.addTranslationReference(self.russian)
        self.english.getTranslations() # cache the translations
        self.english.removeTranslationReference(self.russian)
        translations = self.english.getTranslations()
        self.assertEqual(len(translations), 2)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    if config.CACHE_TRANSLATIONS:
        suite.addTest(makeSuite(TestCanonicalCache))
        suite.addTest(makeSuite(TestTranslationsCache))
    return suite
