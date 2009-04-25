from zope.component import adapts

from Products.Archetypes.interfaces import IReferenceCatalog
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.ZCatalog.exportimport import ZCatalogXMLAdapter


def importCatalogTool(context):
    """Import reference catalog.
    """
    site = context.getSite()
    tool = getToolByName(site, 'reference_catalog', None)
    if tool is not None:
        importObjects(tool, '', context)


def exportCatalogTool(context):
    """Export reference catalog.
    """
    site = context.getSite()
    tool = getToolByName(site, 'reference_catalog', None)
    if tool is None:
        logger = context.getLogger('catalog')
        logger.info('Nothing to export.')
        return

    exportObjects(tool, '', context)


class ReferenceCatalogXMLAdapter(ZCatalogXMLAdapter):
    """XML im- and exporter for the Reference Catalog.
    """

    adapts(IReferenceCatalog, ISetupEnviron)

    _LOGGER_ID = 'reference_catalog'

    name = 'reference_catalog'

    def _initColumns(self, node):
        for child in node.childNodes:
            if child.nodeName != 'column':
                continue
            col = str(child.getAttribute('value'))
            if child.hasAttribute('remove'):
                # Remove the column if it is there
                if col in self.context.schema()[:]:
                    self.context.delColumn(col)
                continue
            if col not in self.context.schema()[:]:
                self.context.addColumn(col)
                # If we added a new column we need to update the
                # metadata even if this will take a while
                self.context.refreshCatalog()
