from Products.LinguaPlone.browser.menu import TranslateMenu
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent


class TranslateMenuTests(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')

    def testLanguageSpecificContentCanBeTranslatedIntoOtherLanguages(self):
        doc = makeContent(self.folder, 'SimpleType', 'doc')
        self.assertEqual(doc.getLanguage(), 'en')
        menu = TranslateMenu('translations')
        self.assertEqual([i['title'] for i in menu.getMenuItems(doc, None)],
            [u'Deutsch', u'label_manage_translations'])
        self.addLanguage('no')
        self.assertEqual([i['title'] for i in menu.getMenuItems(doc, None)],
            [u'Deutsch', u'Norsk', u'label_manage_translations'])

    def testNeutralContentCannotBeTranslatedDirectly(self):
        self.folder.setLanguage('')
        doc = makeContent(self.folder, 'SimpleType', 'doc')
        self.assertEqual(doc.getLanguage(), '')
        menu = TranslateMenu('translations')
        items = menu.getMenuItems(doc, None)
        self.assertEqual([i['title'] for i in items],
            [u'label_manage_translations'])

    def testMenuEmptyForUnauthorizedUsers(self):
        # test menu is empty for unauthorized users:
        self.loginAsPortalOwner()
        doc = makeContent(self.portal, 'SimpleType', 'doc')
        self.login('test_user_1_')
        self.setRoles('Reader')
        menu = TranslateMenu('translations')
        self.assertEqual(menu.getMenuItems(doc, None), [])