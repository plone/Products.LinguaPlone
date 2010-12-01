#
# Functional Tests
#

from Products.LinguaPlone.tests.LinguaPloneTestCase import \
     LinguaPloneFunctionalTestCase


FILES = [
    'create_translation.txt',
    'dynamic_view.txt',
    'language_policies.txt',
    'translate_edit.txt',
    'migration.txt',
]


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    suite = TestSuite()
    for doc_file in FILES:
        suite.addTest(FunctionalDocFileSuite(doc_file,
                      package='Products.LinguaPlone.tests',
                      test_class=LinguaPloneFunctionalTestCase))
    return suite
