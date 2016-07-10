from zope.interface import Interface
from zope.interface import implementer_only
from zope.schema import Choice
from zope.schema import Tuple
from zope.formlib.form import FormFields
from plone.app.controlpanel.language import LanguageControlPanel as BasePanel
from plone.app.controlpanel.language import LanguageControlPanelAdapter
from Products.LinguaPlone import LinguaPloneMessageFactory as _


class IMultiLanguageSelectionSchema(Interface):

    default_language = Choice(
        title=_(u"heading_site_language",
                default=u"Default site language"),
        description=_(u"description_site_language",
                      default=u"The default language used for the content "
                              u"and the UI of this site."),
        required=True,
        vocabulary="LinguaPlone.vocabularies.AllContentLanguageVocabulary")

    available_languages = Tuple(
        title=_(u"heading_available_languages",
                default=u"Available languages"),
        description=_(u"description_available_languages",
                default=u"The languages in which the site should be "
                        u"translatable."),
        required=True,
        missing_value=set(),
        value_type=Choice(
            vocabulary="LinguaPlone.vocabularies.AllContentLanguageVocabulary"))


@implementer_only(IMultiLanguageSelectionSchema)
class MultiLanguageControlPanelAdapter(LanguageControlPanelAdapter):

    def __init__(self, context):
        super(MultiLanguageControlPanelAdapter, self).__init__(context)

    def get_available_languages(self):
        return [unicode(l) for l in self.context.getSupportedLanguages()]

    def set_available_languages(self, value):
        languages = [str(l) for l in value]
        self.context.supported_langs = languages

    available_languages = property(get_available_languages,
                                   set_available_languages)


class LanguageControlPanel(BasePanel):
    """A modified language control panel, allows selecting multiple languages.
    """

    form_fields = FormFields(IMultiLanguageSelectionSchema)
