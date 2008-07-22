# Jarn AS <info@jarn.com>
# http://www.jarn.com

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

"""
Baseclass for multilingual folderish content.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *
from I18NBaseObject import I18NBaseObject

class I18NBaseFolder(I18NBaseObject, BaseFolder):
    """ Base class for translatable objects """
    __implements__ = I18NBaseObject.__implements__ + BaseFolder.__implements__

    security = ClassSecurityInfo()

    def __nonzero__(self):
        return 1

    def manage_beforeDelete(self, item, container):
        I18NBaseObject.manage_beforeDelete(self, item, container)
        BaseFolder.manage_beforeDelete(self, item, container)

    def __browser_default__(self, request):
        """Set default so we can return whatever we want instead of index_html.

        Make sure we use the I18N aware one.
        """
        return getToolByName(self, 'plone_utils').browserDefault(self)


InitializeClass(I18NBaseFolder)
