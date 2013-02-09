from Products.LinguaPlone.I18NBaseObject import TypeInfoWrapper
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent


class TestBaseObject(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('fr')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')

    def test_getTypeInfo(self):
        """
        LinguaPlone uses TypeInfoWrapper to change 'edit' action to
        'translate_item' on non translations.
        """

        ti = self.english.getTypeInfo()
        self.assertTrue(isinstance(ti, TypeInfoWrapper))

    def test_getTypeInfo_nosite(self):
        """
        getTypeInfo should not break when site has not been set
        """
        from zope.site.hooks import getSite
        from zope.site.hooks import setSite

        # save site before unhooking it in order to set it back after the test
        saved_site = getSite()

        setSite(None)

        ti = self.english.getTypeInfo()

        self.assertTrue(isinstance(ti, TypeInfoWrapper))

        # reset site to avoid breaking other tests
        setSite(saved_site)
