from zope.interface import directlyProvides

from Products.CMFCore.utils import getToolByName
from Testing.makerequest import makerequest

from Products.LinguaPlone.browser import controlpanel
from Products.LinguaPlone.interfaces import ILinguaPloneProductLayer
from Products.LinguaPlone.tests.base import LinguaPloneTestCase


class TestLanguageControlPanel(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('no')
        self.setLanguage('en')
        self.langs = set(('de', 'en', 'no'))

    def testRenderControlPanel(self):
        self.loginAsPortalOwner()
        app = makerequest(self.app)
        directlyProvides(app.REQUEST, ILinguaPloneProductLayer)
        panel = self.portal.restrictedTraverse('@@language-controlpanel')
        output = panel()
        self.assert_("Language Settings" in output)
        self.assert_("Default site language" in output)
        self.assert_("Available languages" in output)

    def testRenderNormalControlPanel(self):
        self.loginAsPortalOwner()
        app = makerequest(self.app)
        self.assert_(not ILinguaPloneProductLayer.providedBy(app.REQUEST))
        panel = self.portal.restrictedTraverse('@@language-controlpanel')
        output = panel()
        self.assert_("Language Settings" in output)
        self.assert_("Site language" in output)
        self.assert_("Available languages" not in output)

    def testAvailableLanguages(self):
        adapter = controlpanel.IMultiLanguageSelectionSchema(self.portal)
        self.assertEquals(set(adapter.available_languages), self.langs)
        new = ['en', 'de']
        adapter.available_languages = new
        ltool = getToolByName(self.portal, 'portal_languages')
        self.assertEquals(set(ltool.getSupportedLanguages()), set(new))
