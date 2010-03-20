from AccessControl import ClassSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError: # pragma: no cover
    from Products.Archetypes.public import *


schema = BaseSchema + Schema((

    StringField(
        name = 'contact',
        languageIndependent = True,
        widget = StringWidget(
            description="Enter a contact email address).")),

    TextField(
        name = 'body',
        required = True,
        searchable = True,
        default_output_type = 'text/html',
        allowable_content_types = ('text/plain',
                                  'text/restructured',
                                  'text/html',
                                  'application/msword'),
        widget = RichWidget(
            description="Enter or upload text for the body of the document.")),

    ImageField(
        name = 'image',
        languageIndependent = True,
        widget = ImageWidget(
            description='Image Independent')),

    ImageField(
        name = 'imageDependent',
        languageIndependent = False,
        widget = ImageWidget(
            description='Image Dependent')),

))


class LinguaItem(BaseContent):
    """A simple multilingual archetype"""

    archetypes_name = portal_type = meta_type = 'Lingua Item'
    schema = schema
    security = ClassSecurityInfo()


registerType(LinguaItem, 'LinguaPlone')
