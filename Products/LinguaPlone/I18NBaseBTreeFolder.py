from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.LinguaPlone.I18NBaseObject import I18NBaseObject

class I18NBaseBTreeFolder(I18NBaseObject, BaseBTreeFolder):
    """Base class for translatable objects."""

    security = ClassSecurityInfo()

    def __nonzero__(self):
        return 1

    def manage_beforeDelete(self, item, container):
        I18NBaseObject.manage_beforeDelete(self, item, container)
        BaseBTreeFolder.manage_beforeDelete(self, item, container)

InitializeClass(I18NBaseBTreeFolder)
