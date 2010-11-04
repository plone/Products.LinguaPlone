from zope.component import adapts

from Products.Archetypes.interfaces import IReferenceCatalog
from Products.GenericSetup.interfaces import ISetupEnviron

from Products.LinguaPlone.exportimport import catalog

NAME = 'reference_catalog'


def importCatalogTool(context):
    """Import catalog.
    """
    catalog.importCatalogTool(context, name=NAME)


def exportCatalogTool(context):
    """Export catalog.
    """
    catalog.exportCatalogTool(context, name=NAME)


class ReferenceCatalogXMLAdapter(catalog.CatalogXMLAdapter):
    """XML im- and exporter for the reference catalog.
    """

    adapts(IReferenceCatalog, ISetupEnviron)

    _LOGGER_ID = NAME
    name = NAME
