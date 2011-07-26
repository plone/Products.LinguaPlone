from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.LinguaPlone.public import BaseBTreeFolder
from Products.LinguaPlone.public import BaseContent
from Products.LinguaPlone.public import BaseFolder
from Products.LinguaPlone.public import BaseSchema
from Products.LinguaPlone.public import ImageField
from Products.LinguaPlone.public import LinesField
from Products.LinguaPlone.public import LinesWidget
from Products.LinguaPlone.public import OrderedBaseFolder
from Products.LinguaPlone.public import ReferenceField
from Products.LinguaPlone.public import registerType
from Products.LinguaPlone.public import RichWidget
from Products.LinguaPlone.public import Schema
from Products.LinguaPlone.public import StringField
from Products.LinguaPlone.public import StringWidget
from Products.LinguaPlone.public import TextField


SimpleSchema = BaseSchema + Schema((

    TextField(
        name='body',
        required=True,
        searchable=True,
        default_output_type='text/html',
        allowable_content_types=(
            'text/plain',
            'text/restructured',
            'text/html',
            'application/msword',
        ),
        widget=RichWidget(
            description='Enter or upload text for the body of the document.',
        ),
    ),

    StringField(
        name='contactName',
        languageIndependent=True,
        widget=StringWidget(
            description='Enter a contact person.',
        ),
    ),

    StringField(
        name='contactName2',
        languageIndependent=True,
        widget=StringWidget(
            description='Enter a contact person.',
        ),
    ),

    StringField(
        name='contactName3',
        languageIndependent=True,
        widget=StringWidget(
            description='Enter a contact person.',
        ),
    ),

    StringField(
        name='contactName4',
        languageIndependent=False,
        accessor='getFourthContactName',
        mutator='setFourthContactName',
        widget=StringWidget(
            description='This field has custom accessor and mutator.',
        ),
    ),

    StringField(
        name='contactName5',
        languageIndependent=True,
        accessor='getFifthContactName',
        mutator='setFifthContactName',
        widget=StringWidget(
            description='This field has custom accessor and mutator.',
        ),
    ),

    StringField(
        name='langIndependentInBase',
        languageIndependent=True,
        widget=StringWidget(
            description='This field is language independent in SimpleType.',
        ),
    ),

    StringField(
        name='langIndependentInDerived',
        languageIndependent=False,
        widget=StringWidget(
            description='This field is language dependent in DerivedType.',
        ),
    ),

    StringField(
        name='langIndependentInBoth',
        languageIndependent=True,
        widget=StringWidget(
            description='This field is language independent everywhere.',
        ),
    ),

    ImageField(
        name='image',
        languageIndependent=True,
    ),

    ImageField(
        name='imageDependent',
        languageIndependent=False,
    ),

    ReferenceField(
        name='reference',
        allowed_types=('SimpleType', ),
        languageIndependent = True,
        relationship='referenceType',
    ),

    ReferenceField(
        name='referenceDependent',
        allowed_types=('SimpleType', ),
        languageIndependent = False,
        relationship='referenceDependentType',
    ),

    ReferenceField(
        name='referenceMulti',
        allowed_types=('SimpleType', ),
        languageIndependent = True,
        multiValued = True,
        relationship='referenceType',
    ),

    LinesField(
        name='lines',
        languageIndependent = True,
        widget=LinesWidget(label="Lines"),
    ),

    TextField(
        name='neutralText',
        languageIndependent=True,
        default_output_type='text/html',
        widget=RichWidget(
            description='Enter some text',
        ),
    ),

))


class SimpleType(BaseContent):
    """A simple multilingual archetype"""
    schema = SimpleSchema
    _at_rename_after_creation = True

    def setContactName(self, value, **kw):
        """Set contact name.
        This tests language independent method generation
        """
        self.getField('contactName').set(self, value, **kw)
        self.testing = value

    def getFourthContactName(self):
        """Custom accessor."""
        return 'getFourthContactName'

    def setFourthContactName(self, value, **kw):
        """Custom mutator."""
        self.getField('contactName4').set(self, 'cn4 ' + value, **kw)

    def getFifthContactName(self):
        """Custom accessor."""
        return 'getFifthContactName'

    def setFifthContactName(self, value, **kw):
        """Custom mutator."""
        self.getField('contactName5').set(self, 'cn5 ' + value, **kw)

    def getRawReference(self):
        return self.getField('reference').getRaw(self)

    def getRawReferenceDependent(self):
        return self.getField('referenceDependent').getRaw(self)

registerType(SimpleType, "LinguaPlone")


DerivedSchema = SimpleSchema.copy()
DerivedSchema['langIndependentInBase'].languageIndependent = 0
DerivedSchema['langIndependentInDerived'].languageIndependent = 1


class DerivedType(SimpleType):
    """A derived multilingual archetype"""
    schema = DerivedSchema

registerType(DerivedType, "LinguaPlone")


class SimpleFolder(BaseFolder):
    """A simple folderish multilingual archetype"""
    schema = BaseSchema

registerType(SimpleFolder, "LinguaPlone")


class DynamicFolder(BrowserDefaultMixin, BaseFolder):
    """A simple folderish multilingual archetype"""
    schema = BaseSchema

registerType(DynamicFolder, "LinguaPlone")


class OrderedFolder(OrderedBaseFolder):
    """A simple ordered-folderish multilingual archetype"""
    schema = BaseSchema


registerType(OrderedFolder, "LinguaPlone")


class BTreeFolder(BaseBTreeFolder):
    """A simple btree-folderish multilingual archetype"""
    schema = BaseSchema


registerType(BTreeFolder, "LinguaPlone")


# Non-LP-classes, typical use case when inheriting from LP-aware product
# in a non-LP-aware product
# The key is to not copy the schema directly (as it has translation_mutator)

from Products.Archetypes.public import registerType


NonLPSchema = SimpleSchema.copy() + Schema((
    StringField(
        name='langIndependentInBase',
        languageIndependent=True,
        widget=StringWidget(
            description='This field is language independent in SimpleType.',
        ),
    ),

    StringField(
        name='contactName4',
        languageIndependent=False,
        accessor='getFourthContactName',
        mutator='setFourthContactName',
        widget=StringWidget(
            description='This field has custom accessor and mutator.',
        ),
    ),

    StringField(
        name='contactName5',
        languageIndependent=True,
        accessor='getFifthContactName',
        mutator='setFifthContactName',
        widget=StringWidget(
            description='This field has custom accessor and mutator.',
        ),
    ),
))


class NonLPSimpleType(SimpleType):
    """A simple multilingual archetype"""
    schema = NonLPSchema


registerType(NonLPSimpleType, "LinguaPlone")


# Unregistered types

class UnregSimpleType(BaseContent):
    """A simple multilingual archetype"""
    schema = SimpleSchema

    def getFourthContactName(self):
        """Custom accessor."""
        return 'getFourthContactName'

    def setFourthContactName(self, value, **kw):
        """Custom mutator."""
        self.getField('contactName4').set(self, 'cn4 ' + value, **kw)

    def getFifthContactName(self):
        """Custom accessor."""
        return 'getFifthContactName'

    def setFifthContactName(self, value, **kw):
        """Custom mutator."""
        self.getField('contactName5').set(self, 'cn5 ' + value, **kw)


class UnregDerivedType(UnregSimpleType):
    """A derived multilingual archetype"""
    schema = DerivedSchema
