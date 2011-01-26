from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


def fake_uid():
    return None


class TestMissingUID(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')

    def testIsCanonical(self):
        self.assertEqual(self.english.isCanonical(), True)

    def testIsCanonicalNoUID(self):
        self.english.UID = fake_uid
        self.assertEqual(self.english.isCanonical(), True)

    def testIsGermanCanonical(self):
        self.assertEqual(self.german.isCanonical(), False)

    def testIsGermanCanonicalNoUID(self):
        self.german.UID = fake_uid
        self.assertEqual(self.german.isCanonical(), True)

    def testReferences(self):
        self.assertEquals(len(self.english.getTranslationBackReferences()), 1)
        self.assertEquals(len(self.german.getTranslationReferences()), 1)

    def testReferencesNoUID(self):
        self.english.UID = fake_uid
        self.german.UID = fake_uid
        self.assertEquals(len(self.english.getTranslationBackReferences()), 0)
        self.assertEquals(len(self.german.getTranslationReferences()), 0)
