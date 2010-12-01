from zope.component import adapts

from Products.Archetypes.interfaces import IUIDCatalog
from Products.GenericSetup.interfaces import ISetupEnviron

from Products.LinguaPlone.exportimport import catalog

NAME = 'uid_catalog'


def importCatalogTool(context):
    """Import catalog.
    """
    catalog.importCatalogTool(context, name=NAME)


def exportCatalogTool(context):
    """Export catalog.
    """
    catalog.exportCatalogTool(context, name=NAME)


class UIDCatalogXMLAdapter(catalog.CatalogXMLAdapter):
    """XML im- and exporter for the UID catalog.
    """

    adapts(IUIDCatalog, ISetupEnviron)

    _LOGGER_ID = NAME
    name = NAME
