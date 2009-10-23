from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import OrderedBaseFolder

try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass

from Products.LinguaPlone.I18NBaseObject import I18NBaseObject

class I18NOrderedBaseFolder(I18NBaseObject, OrderedBaseFolder):
    """Base class for translatable objects."""

    security = ClassSecurityInfo()

    def __nonzero__(self):
        return 1

    def manage_beforeDelete(self, item, container):
        I18NBaseObject.manage_beforeDelete(self, item, container)
        OrderedBaseFolder.manage_beforeDelete(self, item, container)

InitializeClass(I18NOrderedBaseFolder)
