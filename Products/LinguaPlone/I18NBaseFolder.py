from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.Archetypes.atapi import BaseFolder
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.I18NBaseObject import I18NBaseObject


class I18NBaseFolder(I18NBaseObject, BaseFolder):
    """ Base class for translatable objects """

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
