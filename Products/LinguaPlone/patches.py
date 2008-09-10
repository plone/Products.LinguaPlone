# Copyright (C) 2004 Helge Tesdal <info@jarn.com>
# Jarn AS http://www.jarn.com

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
Patches.
"""

from Products.LinguaPlone.config import GLOBAL_REQUEST_PATCH
from Products.LinguaPlone.config import I18NAWARE_CATALOG
from Products.LinguaPlone.config import PKG_NAME

_enabled = []

def AlreadyApplied(patch):
    if patch in _enabled:
        return True
    _enabled.append(patch)
    return False


# PATCH 1
#
# Makes REQUEST available from the Globals module.
#
# It's needed because context is not available in the __of__ method,
# so we can't get REQUEST with acquisition. And we need REQUEST for
# local properties (see LocalPropertyManager.pu).
#
# This patch was taken from Localizer (http://www.localizer.org)
# so this software runs indepently of Localizer
#
# The patch is inspired in a similar patch by Tim McLaughlin, see
# "http://dev.zope.org/Wikis/DevSite/Proposals/GlobalGetRequest".
# Thanks Tim!!
#
def GlobalRequestPatch():
    if AlreadyApplied('GlobalRequestPatch'):
        return

    from thread import get_ident
    from ZPublisher import Publish
    from zLOG import LOG, PROBLEM
    import Globals

    def get_request():
        """Get a request object"""
        return Publish._requests.get(get_ident(), None)

    def new_publish(request, module_name, after_list, debug=0):
        id = get_ident()
        Publish._requests[id] = request
        x = Publish.old_publish(request, module_name, after_list, debug)
        try:
            del Publish._requests[id]
        except KeyError:
            # Some people has reported that sometimes a KeyError exception is
            # raised in the previous line, I haven't been able to reproduce it.
            # This try/except clause seems to work. I'd prefer to understand
            # what is happening.
            # MJ: this happens during conflicts; old_publish calls itself with 
            # request.retry() as the new request.
            # TODO: use zope.publisher.browser.setDefaultSkin and weak references
            # instead to track requests.
            LOG(PKG_NAME, PROBLEM,
                "The thread number %s doesn't have an associated request object." % id)
        return x

    if not hasattr(Globals, 'get_request'):
        # Apply patch
        Publish._requests = {}
        Publish.old_publish = Publish.publish
        Publish.publish = new_publish
        Globals.get_request = get_request


# PATCH 2
#
# Patches the catalog tool to filter languages
#
def I18nAwareCatalog():
    if AlreadyApplied('I18nAwareCatalog'):
        return

    from Globals import DTMLFile
    from Products.CMFPlone.CatalogTool import CatalogTool
    from Products.CMFCore.utils import getToolByName

    def searchResults(self, REQUEST=None, **kw):
        """ Calls ZCatalog.searchResults with extra arguments that
            limit the results to what the user is allowed to see.

            This version only returns the results for the current
            language, unless you explicitly ask for all results by
            providing the Language="all" keyword.
        """
        kw = kw.copy()
        languageTool = getToolByName(self, 'portal_languages', None)

        # When searching on certain indexes we don't want language filtering.
        nofilterkeys = ['Language', 'UID', 'id', 'getId']

        def filterSearch(dict, keys=nofilterkeys):
            if not dict:
                return 1
            for key in keys:
                if dict.has_key(key):
                    return 0
            return 1

        if languageTool is not None and filterSearch(REQUEST) and filterSearch(kw):
            try:
                kw['Language'] = [languageTool.getPreferredLanguage(), '']
            except AttributeError:
                pass
        # 'all' deletes the query key
        elif REQUEST and REQUEST.get('Language', '') == 'all':
            del REQUEST['Language']
        elif kw.get('Language', '') == 'all':
            del kw['Language']

        return self.__old_searchResults(REQUEST, **kw)

    CatalogTool.__old_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults
    CatalogTool.manage_catalogView = DTMLFile('www/catalogView',globals())


# PATCH 3
#
# Patches kupu to allow a single portal type to be used as a resource
# type
#
def PortalTypeAsResourceType():
    if AlreadyApplied('PortalTypeAsResourceType'):
        return

    import Products.kupu.plone.plonedrawers

    PREFIX = 'linguaplone-'
    BaseResourceType = Products.kupu.plone.plonedrawers.ResourceType
    class LinguaPloneResourceType(BaseResourceType):
        def __init__(self, tool, name):
            if name.startswith(PREFIX):
                self.name = name
                self._tool = tool
                self._portal_types = name[len(PREFIX):].split(',')
                self._field = self._widget = None
            else:
                BaseResourceType.__init__(self, tool, name)

    Products.kupu.plone.plonedrawers.ResourceType = LinguaPloneResourceType

if GLOBAL_REQUEST_PATCH:
    GlobalRequestPatch()

if I18NAWARE_CATALOG:
    I18nAwareCatalog()

PortalTypeAsResourceType()
