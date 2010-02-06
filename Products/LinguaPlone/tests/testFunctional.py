#
# Functional Tests
#

from Products.LinguaPlone.tests.LinguaPloneTestCase import \
     LinguaPloneFunctionalTestCase


FILES = [
    'create_translation.txt',
    'dynamic_view.txt',
    'translate_edit.txt',
    'migration.txt',
    'language_setup.txt',
]

PLONE40 = False
try:
    from Products.PloneTestCase.version import PLONE40
except ImportError:
    pass

if PLONE40:
    FILES.append('language_policies4.txt')
else:
    FILES.append('language_policies.txt')

def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    suite = TestSuite()
    for doc_file in FILES:
        suite.addTest(FunctionalDocFileSuite(doc_file,
                      package='Products.LinguaPlone.tests',
                      test_class=LinguaPloneFunctionalTestCase))
    return suite
