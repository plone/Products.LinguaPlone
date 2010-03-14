from zope.interface import Attribute
from zope.interface import Interface

from Products.PluginIndexes.interfaces import IPluggableIndex

from plone.theme.interfaces import IDefaultPloneLayer


class ILinguaPloneProductLayer(IDefaultPloneLayer):
    """A layer specific for LinguaPlone.

    We will use this to register browser pages that should only be used
    when LinguaPlone is installed in the site.
    """


class ILanguageIndex(IPluggableIndex):
    """Index for ITranslatable Language tags

    The index treats language tags according to RFC 1766, with the assumption
    that languages with more than one subtag but with the same initial subtag
    as related; en-us is related to en-gb, and will fall back to related
    content (same canonical UID) when queried.

    Language tags are treated as containing a initial subtag, and one optional
    second subtag, splitting a tag on the first dash. Thus, this index does
    not support additional subtags, but modern browsers never send anything
    more complicated than a main language with a region or dialect, nor do
    current Plone i18n tools support anything else.

    Fallback rules are as follows: if searching for a given language tag, a
    union is returned of:

    1. Exact tag match
    2. Initial subtag match, no second subtag (if not the original search)
    3. Any other second subtags indexed for the initial subtag in alfabetical
       order.

    Results are filtered for unique canonical UIDs, thus ensuring only one
    translation per content item is returned.

    So, when searching for en-gb, all matches for en-gb are returned, plus
    any matches for en, en-au, en-ca, en-nz, en-us if such tags were indexed
    and not already translated into en-gb.

    The fallback behaviour can be disabled by setting index.fallback to False,
    or passing a 'fallback' query parameter (also a boolean) to the index
    when querying.

    """

    fallback = Attribute(
        'fallback',
        """Wether or not to enable language fallback querying.

        Boolean, defaults to True.
        """,
        )


class ITranslatable(Interface):
    """
    Interface for translatable content.

    This was originally a Zope2 interface in CMFPlone:
    Products.CMFPlone.interfaces.Translatable.ITranslatable.
    """

    def isTranslation():
        """Return language if this object is used as multilingual content,
        0 otherwise.
        """

    def addTranslation(language, **kwargs):
        """
        Add a new language translation of this content.

        Returns the newly created translation.
        """

    def removeTranslation(language):
        """
        Removes a translation
        """

    def getTranslation(language='language'):
        """
        Return the object corresponding to a translated version or None if no
        translation exists.

        If called without arguments it returns the translation in the currently
        selected language. If the object is already in the selected language
        it returns self.
        """

    def getTranslationLanguages():
        """
        Return a list of language codes
        """

    def getTranslations(include_canonical=True, review_state=True):
        """
        Return a dict of {lang : [object, wf_state]}. If the argument
        include_canonical is False, the canonical object itself won't be
        returned. By default the canonical object is returned. If the
        review_state argument is False, a dict of {lang : object} will be
        returned.
        """

    def isCanonical():
        """
        boolean, is this the original, canonical translation of the content.
        """

    def getCanonicalLanguage():
        """
        Return the language code for the canonical translation of this content.
        """

    def getCanonical():
        """
        Return the original, canonical translation of this content.
        """

    def setLanguage(language):
        """
        Sets the language for the current translation - same as DC
        """

    def Language():
        """
        Returns the language of this translation - same as DC
        """


class ILocateTranslation(Interface):
    context = Attribute("context",
                        "The object that is being translated")

    def findLocationForTranslation(language):
        """Find and return a location for a new translation.

        This may either return an existing location, or create a new folder and
        return that.
        """


class ITranslationFactory(Interface):
    context = Attribute("context",
                        "The object that is being translated")

    def createTranslation(container, language, *args, **kwargs):
        """Create and return a translation.

        The extra arguments are passed to the object creation logic
        and can be used to initialize fields.

        Create a translation of the context for the given language in
        the specicified folder. The new object is returned.

        This method has to setup the translation reference on the
        new object.
        """


class ILanguageIndependentFields(Interface):
    context = Attribute("context", "A translatable object")

    def getFields():
        """Return list of language independent fields"""

    def getFieldsToCopy(translation):
        """Return list of language independent fields to copy to translation.

        The list only includes fields present in both source and destination
        schemas.
        """

    def copyField(field, translation):
        """Copy a language independent field to translation."""

    def copyFields(translation):
        """Copy language independent fields to translation."""
