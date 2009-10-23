from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import BaseContent

try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass

from Products.LinguaPlone.I18NBaseObject import I18NBaseObject


class I18NBaseContent(I18NBaseObject, BaseContent):
    """Overrides BaseContent for *i18n* content."""

    security = ClassSecurityInfo()

    def manage_beforeDelete(self, item, container):
        I18NBaseObject.manage_beforeDelete(self, item, container)
        BaseContent.manage_beforeDelete(self, item, container)

InitializeClass(I18NBaseContent)
