from Testing import ZopeTestCase

# Make sure the dummy types are registered
from Products.LinguaPlone import examples
from Products.LinguaPlone.tests import dummy
ZopeTestCase.installProduct('LinguaPlone')

from Products.GenericSetup import EXTENSION, profile_registry

profile_registry.registerProfile('LinguaPlone_samples',
        'LinguaPlone example content types',
        'Extension profile including sample content types to test LinguaPlone',
        'profiles/sample_types',
        'Products.LinguaPlone',
        EXTENSION)
profile_registry.registerProfile('LinguaPlone_tests',
        'LinguaPlone test content types',
        'Extension profile including dummy types to test LinguaPlone',
        'profiles/test_types',
        'Products.LinguaPlone',
        EXTENSION)


from Products.PloneTestCase import PloneTestCase
from Products.LinguaPlone.tests import utils
from Testing.ZopeTestCase.utils import setupCoreSessions

PORTAL_NAME = 'plone_ml'

PloneTestCase.setupPloneSite(id=PORTAL_NAME, 
        extension_profiles=['Products.LinguaPlone:LinguaPlone',
                            'Products.LinguaPlone:LinguaPlone_tests',
                            'Products.LinguaPlone:LinguaPlone_samples'])


class LinguaPloneTestCase(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.portal.portal_languages.use_cookie_negotiation=1
        self.portal.portal_languages.use_request_negotiation=1

    def getPortal(self):
        return self.app[PORTAL_NAME]

    def _setup(self):
        # Transparently extend the base setup
        PloneTestCase.PloneTestCase._setup(self)
        utils.setupGlobalRequest(self.app.REQUEST)
        setupCoreSessions(self.app)

    def addLanguage(self, language):
        self.portal.portal_languages.addSupportedLanguage(language)

    def setLanguage(self, language):
        request = self.app.REQUEST
        request['set_language'] = language
        self.portal.portal_languages.setLanguageBindings()


class LinguaPloneFunctionalTestCase(ZopeTestCase.Functional, LinguaPloneTestCase):
    pass
