# -*- coding: UTF-8 -*-

import os
from unittest import TestCase


class TestConfig(TestCase):

    def test_relationship_key(self):
        from ..config import RELATIONSHIP
        self.assertEquals(RELATIONSHIP, 'translationOf')

    def test_i18naware_catalog(self):
        from ..config import I18NAWARE_CATALOG
        self.assertEquals(I18NAWARE_CATALOG, True)

    def test_i18naware_catalog_set(self):
        from Products.LinguaPlone import config
        envkey = 'PLONE_I18NAWARE_CATALOG'
        self.assertEquals(config.I18NAWARE_CATALOG, True)
        try:
            os.environ[envkey] = 'false'
            reload(config)
            self.assertEquals(config.I18NAWARE_CATALOG, False)
        finally:
            del os.environ[envkey]
            reload(config)

    def test_nofilterkeys(self):
        from ..config import NOFILTERKEYS
        expected = set(['Language', 'UID', 'id', 'getId'])
        self.assertEquals(set(NOFILTERKEYS), expected)

    def test_reference_fields(self):
        from ..config import I18NAWARE_REFERENCE_FIELDS
        from Products.Archetypes.Field import ReferenceField
        self.assert_(ReferenceField in I18NAWARE_REFERENCE_FIELDS)
