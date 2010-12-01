from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.Archetypes.atapi import OrderedBaseFolder

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
