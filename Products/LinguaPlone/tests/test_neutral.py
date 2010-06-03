#
# Neutral Tests
#

from Products.LinguaPlone.tests import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestNeutral(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.setLanguage('en')
        self.addLanguage('de')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')

    def testContentNotCreatedAsNeutral(self):
        self.failUnlessEqual(self.english.getLanguage(), 'en')

    def testContentSetLanguageToSelectedLanguage(self):
        self.english.setLanguage('de')
        self.failUnlessEqual(self.english.getLanguage(), 'de')

    def testContentSetLanguageToUnselectedLanguage(self):
        self.english.setLanguage('pt-br')
        self.failUnlessEqual(self.english.getLanguage(), 'pt-br')

    def testContentSetLanguageBackToNeutral(self):
        self.english.setLanguage('en')
        self.english.setLanguage('')
        self.failUnlessEqual(self.english.getLanguage(), '')

    def testNeutralIsNotATranslation(self):
        self.failUnlessEqual(self.english.isTranslation(), False)

    def testNeutralRemoveReferences(self):
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')
        self.failUnless('de' in self.english.getTranslationLanguages())
        self.german.setLanguage('')
        self.failUnlessEqual(self.english.getTranslationLanguages(), ['en'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNeutral))
    return suite
