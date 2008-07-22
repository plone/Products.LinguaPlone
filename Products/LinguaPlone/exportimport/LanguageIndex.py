# Plone Solutions AS <info@plonesolutions.com>
# Martijn Pieters <mj@plonesolutions.com>
# http://www.plonesolutions.com

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from Products.GenericSetup.utils import NodeAdapterBase, PropertyManagerHelpers

from Products.LinguaPlone.interfaces import ILanguageIndex

class LanguageIndexNodeAdapter(NodeAdapterBase, PropertyManagerHelpers):

    """Node im- and exporter for LanguageIndex.
    """

    __used_for__ = ILanguageIndex

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
