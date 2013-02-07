
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestGeneratedMethods(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('fr')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.alsoenglish = makeContent(self.folder, 'SimpleType', 'doctwo')
        self.alsoenglish.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')
        self.french = makeContent(self.folder, 'SimpleType', 'frenchdoc')
        self.french.setLanguage('fr')
        self.folder_en = makeContent(self.folder, 'SimpleFolder', 'folder')
        self.folder_en.setLanguage('en')

    def test_setModificationDate(self):
        """
        LinguaPlone autogenerates a method for setModificationDate overriding
        the one present at Products.Archetypes.ExtensibleMetadata.
        This method in Archetypes has a default value for a parameter and it
        handles it autogenerating the modification date.
        This test shows that if you call setModificationDate without a parameter
        it will call the field default value
        """
        from DateTime import DateTime
        now = DateTime()

        self.english.setModificationDate(now)
        self.assertEqual(self.english.modified(), now)
        self.english.setModificationDate()
        self.failUnless(self.english.modified() > now)
