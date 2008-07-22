#
# Language Independent Tests
#

from Products.LinguaPlone.tests import LinguaPloneTestCase
from Products.LinguaPlone.tests import dummy
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestLanguageIndependentFields(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        # Speed things up
        self.portal._delObject('portal_catalog')

    def testLanguageIndependentField(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')

        contact = 'Test string'
        english.setTitle('English title')
        english.setContactName(contact)
        german.setTitle('German title')
        self.failIfEqual(english.Title(), german.Title())
        self.assertEqual(english.getContactName(), contact)
        self.assertEqual(english.getRawContactName(), contact)
        self.assertEqual(german.getContactName(), contact)
        self.assertEqual(german.getRawContactName(), contact)
        self.failUnless(english.contactName)
        self.failUnless(german.contactName)
        self.failUnless(hasattr(german, 'testing'))
        self.assertEqual(german.testing, english.contactName)
        self.assertEqual(english.contactName, german.contactName)

        contact = 'First name'
        german.setContactName(contact)
        self.assertEqual(english.getContactName(), contact)
        self.assertEqual(english.getRawContactName(), contact)
        self.assertEqual(german.getContactName(), contact)
        self.assertEqual(german.getRawContactName(), contact)
        self.failUnless(english.contactName)
        self.failUnless(german.contactName)
        self.failUnless(hasattr(english, 'testing'))
        self.assertEqual(english.testing, german.contactName)
        self.assertEqual(english.contactName, german.contactName)

    # Test derived type

    def testBaseSchemaSetup(self):
        schema = dummy.SimpleType.schema
        self.assertEqual(schema['langIndependentInBase'].languageIndependent, 1)
        self.assertEqual(schema['langIndependentInDerived'].languageIndependent, 0)
        self.assertEqual(schema['langIndependentInBoth'].languageIndependent, 1)

    def testDerivedSchemaSetup(self):
        schema = dummy.DerivedType.schema
        self.assertEqual(schema['langIndependentInBase'].languageIndependent, 0)
        self.assertEqual(schema['langIndependentInDerived'].languageIndependent, 1)
        self.assertEqual(schema['langIndependentInBoth'].languageIndependent, 1)

    def testLangIndependentInBase(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        teststring = 'Test string'
        # When overriding languageIndependent from base class, the original
        # translation aware mutator actually checks for language independence
        english.setLangIndependentInBase(teststring)
        self.failIfEqual(german.getLangIndependentInBase(), teststring)
        self.failIfEqual(german.getRawLangIndependentInBase(), teststring)

    def testLangIndependentInDerived(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        teststring = 'Test string'
        # Note that you *can* override a 'false' languageIndependent field
        # from a base class...
        english.setLangIndependentInDerived(teststring)
        self.assertEqual(german.getLangIndependentInDerived(), teststring)
        self.assertEqual(german.getRawLangIndependentInDerived(), teststring)

    def testLangIndependentInBoth(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        teststring = 'Test string'
        english.setLangIndependentInBoth(teststring)
        self.assertEqual(german.getLangIndependentInBoth(), teststring)
        self.assertEqual(german.getRawLangIndependentInBoth(), teststring)

    # Test content that is not LP-aware
    def testLangIndependentGeneratedMethodsInNonLP(self):
        english = makeContent(self.folder, 'NonLPSimpleType', 'doc')
        english.setLanguage('en')
        teststring = 'Test string'
        # If this fails, you can't inherit unless you also get a copy of the schema
        english.setLangIndependentInBase(teststring)
        self.assertEqual(english.getLangIndependentInBase(), teststring)
        self.assertEqual(english.getRawLangIndependentInBase(), teststring)

    def testNotLangIndependentCustomMethodsInNonLP(self):
        english = makeContent(self.folder, 'NonLPSimpleType', 'doc')
        english.setLanguage('en')
        teststring = 'Test string'
        # If this fails, you can't inherit unless you also get a copy of the schema
        english.setFourthContactName(teststring)
        self.assertEqual(english.getFourthContactName(), 'getFourthContactName')
        self.assertEqual(str(english.contactName4), 'cn4 %s' % teststring)

    def testLangIndependentCustomMethodsInNonLP(self):
        english = makeContent(self.folder, 'NonLPSimpleType', 'doc')
        english.setLanguage('en')
        teststring = 'Test string'
        # If this fails, you can't inherit unless you also get a copy of the schema
        english.setFifthContactName(teststring)
        self.assertEqual(english.getFifthContactName(), 'getFifthContactName')
        # The original method is not detected properly... annotate?
        # Annotate the generated method!!!! provide original method name
        self.assertEqual(str(english.contactName5), 'cn5 %s' % teststring)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLanguageIndependentFields))
    return suite
