from plone.i18n.locales.interfaces import IContentLanguageAvailability
from plone.i18n.locales.interfaces import IMetadataLanguageAvailability
from zope.component import queryUtility

from Products.LinguaPlone.tests import LinguaPloneTestCase


class TestVocabularies(LinguaPloneTestCase.LinguaPloneTestCase):

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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestVocabularies))
    return suite
