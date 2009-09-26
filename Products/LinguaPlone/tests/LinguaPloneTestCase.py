from Testing import ZopeTestCase

# Make sure the dummy types are registered
from Products.LinguaPlone import examples
from Products.LinguaPlone.tests import dummy

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

from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase

PORTAL_NAME = 'plone'

ZopeTestCase.utils.setupCoreSessions()
ZopeTestCase.installProduct('LinguaPlone')

@onsetup
def setup_product():
    PloneTestCase.installPackage('plone.browserlayer', quiet=1)

extension_profiles=['Products.LinguaPlone:LinguaPlone',
                    'Products.LinguaPlone:LinguaPlone_tests',
                    'Products.LinguaPlone:LinguaPlone_samples']

setup_product()
PloneTestCase.setupPloneSite(id=PORTAL_NAME,
        extension_profiles=extension_profiles)


class LinguaPloneTestCase(PloneTestCase.PloneTestCase):

    def getPortal(self):
        return self.app[PORTAL_NAME]

    def addLanguage(self, language):
        self.portal.portal_languages.addSupportedLanguage(language)

    def setLanguage(self, language):
        request = self.app.REQUEST
        request['set_language'] = language
        self.portal.portal_languages.setLanguageBindings()


class LinguaPloneFunctionalTestCase(ZopeTestCase.Functional, LinguaPloneTestCase):
    pass

