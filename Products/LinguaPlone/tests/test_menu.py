from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.browser.menu import TranslateMenu


class TranslateMenuTests(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')

    def testLanguageSpecificContentCanBeTranslatedIntoOtherLanguages(self):
        doc = makeContent(self.folder, 'SimpleType', 'doc')
        self.assertEqual(doc.getLanguage(), 'en')
        menu = TranslateMenu('translations')
        self.assertEqual([i['title'] for i in menu.getMenuItems(doc, None)],
            [u'German', u'label_manage_translations'])
        self.addLanguage('no')
        self.assertEqual([i['title'] for i in menu.getMenuItems(doc, None)],
            [u'German', u'Norwegian', u'label_manage_translations'])


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
