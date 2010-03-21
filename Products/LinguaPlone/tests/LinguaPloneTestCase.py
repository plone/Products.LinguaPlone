from Testing import ZopeTestCase
from Testing.ZopeTestCase import Functional

# Make sure the dummy types are registered
from Products.LinguaPlone import examples; examples
from Products.LinguaPlone.tests import dummy; dummy

from Products.Five import zcml
from Products.Five import fiveconfigure
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

PLONE40 = False
try:
    from Products.PloneTestCase.version import PLONE40
except ImportError:
    pass


ZopeTestCase.installProduct('LinguaPlone')


@onsetup
def setup_product():
    PloneTestCase.installPackage('plone.browserlayer', quiet=1)
    fiveconfigure.debug_mode = True
    import Products.LinguaPlone.tests
    zcml.load_config('configure.zcml', Products.LinguaPlone.tests)
    fiveconfigure.debug_mode = False

extension_profiles=['Products.LinguaPlone:LinguaPlone',
                    'Products.LinguaPlone:LinguaPlone_tests',
                    'Products.LinguaPlone:LinguaPlone_samples']

setup_product()
PloneTestCase.setupPloneSite(extension_profiles=extension_profiles)


class LinguaPloneTestCase(PloneTestCase.PloneTestCase):

    def addLanguage(self, language):
        self.portal.portal_languages.addSupportedLanguage(language)

    def setLanguage(self, language):
        request = self.app.REQUEST
        request['set_language'] = language
        self.portal.portal_languages.setLanguageBindings()


class LinguaPloneFunctionalTestCase(Functional, LinguaPloneTestCase):
    pass


__all__ = (LinguaPloneTestCase, LinguaPloneFunctionalTestCase, PLONE40, )
