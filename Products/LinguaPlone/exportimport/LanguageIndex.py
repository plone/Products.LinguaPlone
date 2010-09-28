from zope.component import adapts

from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import NodeAdapterBase
from Products.GenericSetup.utils import PropertyManagerHelpers

from Products.LinguaPlone.interfaces import ILanguageIndex


class LanguageIndexNodeAdapter(NodeAdapterBase, PropertyManagerHelpers):
    """Node im- and exporter for LanguageIndex.
    """

    adapts(ILanguageIndex, ISetupEnviron)

    def _exportNode(self):
        """Export the object as a DOM node."""

        node = self._getObjectNode('index')
        node.appendChild(self._extractProperties())
        return node

    def _importNode(self, node):
        """Import the object from the DOM node."""

        if self.environ.shouldPurge():
            self._purgeProperties()

        self._initProperties(node)
        self.context.clear()

    node = property(_exportNode, _importNode)
