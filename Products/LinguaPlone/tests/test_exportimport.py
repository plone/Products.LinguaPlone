import unittest

from Products.GenericSetup.testing import NodeAdapterTestCase
from Products.GenericSetup.testing import ExportImportZCMLLayer


_LANGUAGE_XML = """\
<index name="foo_language" meta_type="LanguageIndex">
 <property name="fallback">True</property>
</index>
"""


class LinguaPloneExportImportLayer(ExportImportZCMLLayer):

    @classmethod
    def setUp(cls):
        from Products.Five import zcml
        import Products.LinguaPlone.exportimport
        zcml.load_config('configure.zcml', Products.LinguaPlone.exportimport)

    @classmethod
    def tearDown(cls):
        pass


class LanguageIndexAdapterTests(NodeAdapterTestCase, unittest.TestCase):

    layer = LinguaPloneExportImportLayer

    def _getTargetClass(self):
        from Products.LinguaPlone.exportimport.LanguageIndex \
                    import LanguageIndexNodeAdapter
        return LanguageIndexNodeAdapter

    def setUp(self):
        from Products.LinguaPlone.LanguageIndex import LanguageIndex
        self._obj = LanguageIndex('foo_language')
        self._XML = _LANGUAGE_XML
