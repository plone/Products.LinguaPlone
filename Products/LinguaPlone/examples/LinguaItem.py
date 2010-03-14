from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

schema = BaseSchema + Schema((
    StringField('contact',
                languageIndependent = 1,
                widget = StringWidget(
                    description="Enter a contact email address (this field is "
                                "language independent)."),
               ),
    TextField('body',
              required = 1,
              searchable = 1,
              default_output_type = 'text/html',
              allowable_content_types = ('text/plain',
                                         'text/restructured',
                                         'text/html',
                                         'application/msword'),
              widget = RichWidget(description="Enter or upload text for the"
                                              " body of the document."),
             ),

    ImageField(
        name='image',
        languageIndependent=True,
        widget=ImageWidget(
            description='Image Independent',
        ),
    ),

    ImageField(
        name='imageDependent',
        languageIndependent=False,
        widget=ImageWidget(
            description='Image Dependent',
        ),
    ),

))


class LinguaItem(BaseContent):
    """A simple multilingual archetype"""
    archetypes_name = portal_type = meta_type = 'Lingua Item'
    schema = schema

    actions = [
        {'id': 'edit',
         'name': 'Edit',
         'action': 'string:${object_url}/base_edit',
         'condition':
            'python: object.isTranslatable() and object.isCanonical()',
         'permissions': (ModifyPortalContent, ),
        },
       {'id': 'translate',
        'name': 'Edit',
        'action': 'string:${object_url}/translate_item',
        'condition':
            'python:object.isTranslatable() and not object.isCanonical()',
        'permissions': (ModifyPortalContent, ),
        },
    ]

    security = ClassSecurityInfo()

registerType(LinguaItem, 'LinguaPlone')
