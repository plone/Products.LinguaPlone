#
# Skeleton Tests
#

from Products.LinguaPlone.tests import LinguaPloneTestCase


class TestSomeProduct(LinguaPloneTestCase.LinguaPloneTestCase):

    def afterSetUp(self):
        pass

    def testSomething(self):
        # Test something
        self.assertEqual(1+1, 2)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSomeProduct))
    return suite

