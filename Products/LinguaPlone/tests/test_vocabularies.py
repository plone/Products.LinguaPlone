from plone.i18n.locales.interfaces import IContentLanguageAvailability
from plone.i18n.locales.interfaces import IMetadataLanguageAvailability
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestSyncedVocabularies(LinguaPloneTestCase):

    def afterSetUp(self):
        self.setLanguage('en')
        self.addLanguage('de')
        self.addLanguage('no')
        self.langs = set(('de', 'en', 'no'))

    def testContentLanguages(self):
        util = queryUtility(IContentLanguageAvailability)
        self.assertEquals(set(util.getAvailableLanguages()), self.langs)
        self.assertEquals(set(util.getLanguages().keys()), self.langs)
        listing = util.getLanguageListing()
        self.assertEquals(set([k[0] for k in listing]), self.langs)

    def testMetadataLanguages(self):
        util = queryUtility(IMetadataLanguageAvailability)
        self.assertEquals(set(util.getAvailableLanguages()), self.langs)
        self.assertEquals(set(util.getLanguages().keys()), self.langs)
        listing = util.getLanguageListing()
        self.assertEquals(set([k[0] for k in listing]), self.langs)


class TestLanguageVocabularies(LinguaPloneTestCase):

    def afterSetUp(self):
        self.setLanguage('en')
        self.addLanguage('de')
        self.addLanguage('no')
        self.langs = set(('de', 'en', 'no'))
        self.ltool = getToolByName(self.portal, 'portal_languages')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')
        self.german.setLanguage('de')

    def testAllContentLanguages(self):
        name = "LinguaPlone.vocabularies.AllContentLanguageVocabulary"
        util = queryUtility(IVocabularyFactory, name=name)
        tokens = util(self.portal).by_token
        self.assert_(len(tokens) > 100)
        self.assert_(len(tokens) < 200)
        self.assert_('en' in tokens)
        self.assert_('en-gb' not in tokens)
        # Test combined languages
        self.ltool.use_combined_language_codes = True
        tokens = util(self.portal).by_token
        self.assert_(len(tokens) > 350)
        self.assert_('en-gb' in tokens)

    def testUntranslatedLanguages(self):
        name="LinguaPlone.vocabularies.UntranslatedLanguages"
        util = queryUtility(IVocabularyFactory, name=name)
        tokens = util(self.english).by_token
        self.assertEquals(len(tokens), 1)
        self.assert_('no' in tokens)

    def testNeutralAndUntranslatedLanguages(self):
        name="LinguaPlone.vocabularies.NeutralAndUntranslatedLanguages"
        util = queryUtility(IVocabularyFactory, name=name)
        tokens = util(self.english).by_token
        self.assertEquals(len(tokens), 2)
        self.assert_('no' in tokens)
        self.assert_('neutral' in tokens)

    def testNoChangeNeutralAndUntranslatedLanguages(self):
        name="LinguaPlone.vocabularies.NoChangeNeutralAndUntranslatedLanguages"
        util = queryUtility(IVocabularyFactory, name=name)
        tokens = util(self.english).by_token
        self.assertEquals(len(tokens), 3)
        self.assert_('no' in tokens)
        self.assert_('neutral' in tokens)
        self.assert_('nochange' in tokens)

    def testDeletableLanguages(self):
        name="LinguaPlone.vocabularies.DeletableLanguages"
        util = queryUtility(IVocabularyFactory, name=name)
        tokens = util(self.english).by_token
        self.assertEquals(len(tokens), 1)
        self.assert_('de' in tokens)
