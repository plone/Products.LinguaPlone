from AccessControl import ClassSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *


schema = BaseSchema


class LinguaFolder(BaseFolder):
    """A simple folderish multilingual archetype"""
    archetypes_name = portal_type = meta_type = 'Lingua Folder'
    schema = schema

    security = ClassSecurityInfo()


registerType(LinguaFolder, 'LinguaPlone')
