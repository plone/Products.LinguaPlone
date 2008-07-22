from zope.interface import Interface
from zope import schema
from zope.formlib import form
from zope.i18nmessageid import Message, MessageFactory
from zope.app.form.browser.itemswidgets import RadioWidget
from zope.app.form.browser.itemswidgets import MultiCheckBoxWidget

from Products.Five.formlib.formbase import FormBase


_ = MessageFactory('linguaplone')


class MyRadioWidget(RadioWidget):
    _displayItemForMissingValue = False
    missing = "nochange"
    def __init__(self, field, request):
        super(MyRadioWidget, self).__init__(field, field.source, request)


class MyMultiCheckBoxWidget(MultiCheckBoxWidget):
    _displayItemForMissingValue = False
    def __init__(self, field, request):
        super(MyMultiCheckBoxWidget, self).__init__(field, field.source, request)


class IManageTranslations(Interface):
    """Interface for the manage translations form."""

    content_language = schema.Choice(
        title=_("header_change_language", default=u"Change content language"),
        description=_(
            "description_change_language",
            default=u"Select the language you want to change the content to.",
        ),
        required=False,
        vocabulary='LinguaPlone.vocabularies.NoChangeNeutralAndUntranslatedLanguages',
    )

    remove_translation = schema.Choice(
        title=_("header_remove_translations", default=u"Remove translations"),
        description=_(
            "description_remove_translations",
            default=u"Select translations to remove.",
        ),
        required=False,
        vocabulary='LinguaPlone.vocabularies.DeletableLanguages',
    )


class ManageTranslationsForm(FormBase):
    form_fields = form.FormFields(IManageTranslations)
    form_fields['content_language'].custom_widget = MyRadioWidget
    form_fields['remove_translation'].custom_widget = MyMultiCheckBoxWidget
    label = _(
        "header_manage_translations",
        default=u"Manage translations",
    )
    description = _(
        "description_manage_translations",
        default=(u"Here you can change the content language or remove "
                  "existing translations."),
    )

    @form.action(Message("label_update", domain="plone", default=u"Update"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        return ''
