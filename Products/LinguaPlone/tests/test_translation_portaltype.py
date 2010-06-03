#
# ITranslationPortalType tests
#

from Testing.ZopeTestCase import ZopeDocTestSuite
from Products.LinguaPlone.tests import LinguaPloneTestCase

def testTranslationPortalType():
    """
    We can create a document

      >>> _ = folder.invokeFactory('Document', id='fred')
      >>> fred = folder.fred

    And translate it

      >>> fred_no = fred.addTranslation('no')

    Now compare portal types

      >>> fred.portal_type
      'Document'

      >>> fred_no.portal_type
      'Document'

    We can register a more specific TranslationFactory to create translation
    objects with e.g. different portal_type.

      >>> from Products.LinguaPlone.interfaces import ITranslationFactory
      >>> from Products.LinguaPlone.utils import TranslationFactory

      >>> class MyTranslationFactory(TranslationFactory):
      ...     def getTranslationPortalType(self, container, language):
      ...         return 'News Item'

      >>> from zope.component import globalSiteManager as gsm
      >>> from Products.ATContentTypes.interface import IATDocument

      >>> gsm.registerAdapter(MyTranslationFactory,
      ...                     required=(IATDocument,),
      ...                     provided=ITranslationFactory)

    Now translate again

      >>> fred_de = fred.addTranslation('de')
      >>> fred_de.portal_type
      'News Item'

    qed

    [Cleanup: Get rid of the adapter]

      >>> gsm.unregisterAdapter(MyTranslationFactory,
      ...                       required=(IATDocument,),
      ...                       provided=ITranslationFactory)
      True
    """


def test_suite():
    return ZopeDocTestSuite(test_class=LinguaPloneTestCase.LinguaPloneTestCase)
