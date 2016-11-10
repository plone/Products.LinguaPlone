from Products.LinguaPlone.tests.base import LinguaPloneFunctionalTestCase


FILES = [
    'create_translation.txt',
    'default_page.txt',
    'dynamic_view.txt',
    'translate_edit.txt',
    'language_setup.txt',
    'language_policies.txt',
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
