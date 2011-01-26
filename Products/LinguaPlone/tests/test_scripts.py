from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestLanguageLists(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('fr')
        self.addLanguage('es')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')

    def testGetTranslatedLanguagesDefault(self):
        # List should contain only the canonical translation
        langs = self.english.getTranslatedLanguages()
        langs = [l[0] for l in langs]
        self.assertEqual(langs, ['en'])

    def testGetTranslatedLanguages(self):
        # List should contain all existing translations
        makeTranslation(self.english, 'de')
        makeTranslation(self.english, 'fr')
        langs = self.english.getTranslatedLanguages()
        langs = [l[0] for l in langs]
        self.assertEqual(set(langs), set(['de', 'en', 'fr']))

    def testGetTranslatedLanguagesWithNoLanguage(self):
        # List should be emtpy, no language defined
        # Fake a translatable object without a language defined
        self.english.setLanguage('')
        langs = self.english.getTranslatedLanguages()
        self.assertEqual(langs, [])

    def testGetTranslatedLanguagesWithUnusedLanguage(self):
        # List should be emtpy, pt is not selected at portal_languages
        self.english.setLanguage('pt')
        langs = self.english.getTranslatedLanguages()
        self.assertEqual(langs, [])

    def testGetUntranslatedLanguagesEmpty(self):
        # List should be emtpy
        makeTranslation(self.english, 'de')
        makeTranslation(self.english, 'fr')
        makeTranslation(self.english, 'es')
        langs = self.english.getUntranslatedLanguages()
        self.assertEqual(langs, [])

    def testGetUntranslatedLanguages(self):
        # List should contain all translations waiting to be done
        makeTranslation(self.english, 'de')
        langs = self.english.getUntranslatedLanguages()
        langs = [l[0] for l in langs]
        self.assertEqual(set(langs), set(['es', 'fr']))

    def testGetDeletableLanguagesEmpty(self):
        # List should be emtpy
        langs = self.english.getDeletableLanguages()
        self.assertEqual(langs, [])

    def testGetDeletableLanguages(self):
        # List should contain all translations except the canonical one
        makeTranslation(self.english, 'de')
        makeTranslation(self.english, 'fr')
        langs = self.english.getDeletableLanguages()
        langs = [l['id'] for l in langs]
        self.assertEqual(set(langs), set(['de', 'fr']))
