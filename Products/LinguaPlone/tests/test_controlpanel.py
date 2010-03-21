from zope.interface import directlyProvides

from Testing.makerequest import makerequest

from Products.LinguaPlone.interfaces import ILinguaPloneProductLayer
from Products.LinguaPlone.tests import LinguaPloneTestCase


class TestLanguageControlPanel(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('no')
        self.setLanguage('en')

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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLanguageControlPanel))
    return suite
