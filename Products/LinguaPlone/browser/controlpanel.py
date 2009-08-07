from zope.interface import Interface
from zope.interface import implementsOnly
from zope.schema import Choice
from zope.schema import Tuple
from zope.formlib.form import FormFields
from plone.app.controlpanel.language import LanguageControlPanel as BasePanel
from plone.app.controlpanel.language import LanguageControlPanelAdapter
from Products.LinguaPlone import LinguaPloneMessageFactory as _


class IMultiLanguageSelectionSchema(Interface):
#    use_combined_language_codes = ILanguageSelectionSchema.use_combined_language_codes

    default_language = Choice(
        title=_(u"heading_site_language",
                default=u"Default site language"),
        description=_(u"description_site_language",
                      default=u"The default language used for the content "
                              u"and the UI of this site."),
        required=True,
        vocabulary="plone.app.vocabularies.AvailableContentLanguages")

    available_languages = Tuple(
        title=_(u"heading_available_languages",
                default=u"Available languages"),
        description=_(u"description_available_languages",
                default=u"The languages in which the site should be "
                        u"translatable."),
        required=True,
        missing_value=set(),
        value_type=Choice(
            vocabulary="plone.app.vocabularies.AvailableContentLanguages"))



class MultiLanguageControlPanelAdapter(LanguageControlPanelAdapter):
    implementsOnly(IMultiLanguageSelectionSchema)

    def __init__(self, context):
        super(MultiLanguageControlPanelAdapter, self).__init__(context)

    def get_available_languages(self):
        return self.context.getSupportedLanguages()

    def set_available_languages(self, value):
        self.context.removeSupportedLanguages(
                    self.context.getSupportedLanguages())

        for lang in value:
            self.context.addSupportedLanguage(lang)

    available_languages = property(get_available_languages,
                                   set_available_languages)




class LanguageControlPanel(BasePanel):
    """A modified language control panel, allows selecting multiple languages.
    """

    form_fields = FormFields(IMultiLanguageSelectionSchema)

    # XXX: We can not use LanguageDropdownChoiceWidget since (as of Plone 3.0.6)
    # pulls its data from IUserPreferredLanguages, which does not use the
    # plone.i18n vocabs to get the proper language names.
    # form_fields['default_language'].custom_widget = LanguageDropdownChoiceWidget

