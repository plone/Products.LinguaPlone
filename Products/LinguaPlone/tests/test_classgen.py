from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests import dummy
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.utils import generateClass


def is_generated(method):
    return getattr(method, '_lp_generated', False)


def is_renamed(method):
    return getattr(method, '_lp_renamed', False)


class TestClassGen(LinguaPloneTestCase):

    def test_A_SimpleType(self):
        klass = dummy.UnregSimpleType
        generateClass(klass)

        # All of these exist in SimpleType
        self.failUnless('getFifthContactName' in klass.__dict__)
        self.failUnless('setFifthContactName' in klass.__dict__)
        self.failUnless('getRawContactName5' in klass.__dict__)
        self.failUnless('setTranslationContactName5' in klass.__dict__)

        # No defaults for contact name
        self.failIf('getContactName5' in klass.__dict__)
        self.failIf('setContactName5' in klass.__dict__)

        # Custom accessor
        self.failIf(is_generated(klass.getFifthContactName))

        # Newly generated mutator forwarding to translation mutators
        self.failUnless(is_generated(klass.setFifthContactName))

        # Renamed setFifthContactName used as translation mutator
        self.failIf(is_generated(klass.setTranslationContactName5))
        self.failUnless(is_renamed(klass.setTranslationContactName5))

    def test_B_DerivedType(self):
        klass = dummy.UnregDerivedType
        generateClass(klass)

        # Inherited custom accessor
        self.failIf('getFifthContactName' in klass.__dict__)

        # The rest exists in DerivedType
        self.failUnless('setFifthContactName' in klass.__dict__)
        self.failUnless('getRawContactName5' in klass.__dict__)
        self.failUnless('setTranslationContactName5' in klass.__dict__)

        # No defaults for contact name
        self.failIf('getContactName5' in klass.__dict__)
        self.failIf('setContactName5' in klass.__dict__)

        # Inherited custom accessor
        self.failIf(is_generated(klass.getFifthContactName))

        # Newly generated mutator...
        self.failUnless(is_generated(klass.setFifthContactName))
        self.failUnless(is_generated(klass.setTranslationContactName5))


class TestCustomAccessors(LinguaPloneTestCase):

    # Do custom accessors work?

    def testLanguageDependentCustomAccessor(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        self.assertEqual(english.getFourthContactName(),
                         'getFourthContactName')

    def testLanguageIndependentCustomAccessor(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        self.assertEqual(english.getFifthContactName(), 'getFifthContactName')

    def testLanguageDependentCustomAccessorDerived(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        self.assertEqual(english.getFourthContactName(),
                         'getFourthContactName')

    def testLanguageIndependentCustomAccessorDerived(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        self.assertEqual(english.getFifthContactName(), 'getFifthContactName')
