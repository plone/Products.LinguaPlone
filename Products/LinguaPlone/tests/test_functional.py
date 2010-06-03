#
# Functional Tests
#

from Products.LinguaPlone.tests.LinguaPloneTestCase import PLONE40
from Products.LinguaPlone.tests.LinguaPloneTestCase import \
     LinguaPloneFunctionalTestCase


FILES = [
    'create_translation.txt',
    'dynamic_view.txt',
    'translate_edit.txt',
    'migration.txt',
    'language_setup.txt',
]

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
