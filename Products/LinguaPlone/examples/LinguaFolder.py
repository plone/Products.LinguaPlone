from AccessControl import ClassSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError: # pragma: no cover
    from Products.Archetypes.public import *


class LinguaFolder(BaseFolder):
    """A simple folderish multilingual archetype"""

    archetypes_name = portal_type = meta_type = 'Lingua Folder'
    schema = BaseSchema
    security = ClassSecurityInfo()


registerType(LinguaFolder, 'LinguaPlone')
