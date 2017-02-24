from zope.component import getGlobalSiteManager
from Products.ATContentTypes.interfaces import IATDocument

from Products.LinguaPlone.interfaces import ITranslationFactory
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.utils import TranslationFactory


class MyTranslationFactory(TranslationFactory):

    def getTranslationPortalType(self, container, language):
        return 'News Item'


class TestTranslationPortalType(LinguaPloneTestCase):

    def testTranslationPortalType(self):
        # We can create a document and translate it
        self.folder.invokeFactory('Document', id='fred')
        fred = self.folder.fred
        fred_no = fred.addTranslation('no')

        self.assertEquals(fred.portal_type, 'Document')
        self.assertEquals(fred_no.portal_type, 'Document')

        # We can register a more specific TranslationFactory to create
        # translation objects with e.g. different portal_type.
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(MyTranslationFactory,
                            required=(IATDocument, ),
                            provided=ITranslationFactory)

        # Now translate again
        fred_de = fred.addTranslation('de')
        self.assertEquals(fred_de.portal_type, 'News Item')

    def beforeTearDown(self):
        gsm = getGlobalSiteManager()
        gsm.unregisterAdapter(MyTranslationFactory,
            required=(IATDocument, ),
            provided=ITranslationFactory)
