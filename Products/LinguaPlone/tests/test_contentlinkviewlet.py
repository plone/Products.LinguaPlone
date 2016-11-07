from zope.interface import directlyProvides

from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation
from Products.LinguaPlone.interfaces import ILinguaPloneProductLayer

from Products.LinguaPlone.browser.contentlinkviewlet import MultilingualContentViewlet

class TestContentLinkViewlet(LinguaPloneTestCase):

    def afterSetUp(self):
        directlyProvides(self.portal.REQUEST, ILinguaPloneProductLayer)
        self.addLanguage('de')
        self.setLanguage('en')
        self.folder.setLanguage('')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')

    def testViewletGeneratesTranslationList(self):
        viewlet = MultilingualContentViewlet(self.english, self.app.REQUEST, None, None)
        viewlet.update()
        self.failIf(getattr(viewlet, 'translations', None) is None)

    def testViewletGeneratedLinks(self):
        viewlet = MultilingualContentViewlet(self.english, self.app.REQUEST, None, None)
        viewlet.update()
        self.assertEqual(len(viewlet.translations), 2)
