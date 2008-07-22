##parameters=link_language=None,link_content=None
##title=

from Products.CMFPlone.utils import transaction_note
REQUEST = context.REQUEST

translation = context.reference_catalog.lookupObject(link_content)

if translation is None:
    message = context.translate(msgid='message_content_not_found',
                                default="Translation content not found.",
                                domain='linguaplone')
    return state.set(status='failure', portal_status_message=message)

if link_language not in context.portal_languages.getSupportedLanguages():
    message = context.translate(msgid='message_invalid_language',
                                default="Invalid language.",
                                domain='linguaplone')
    return state.set(status='failure', portal_status_message=message)

# Unlink from current translations
translation.setLanguage('')

# Set new language, and link to current object
translation.setLanguage(link_language)
canonical = context.getCanonical()
translation.addTranslationReference(canonical)

title = translation.Title()
language = context.portal_languages.getNameForLanguageCode(link_language)

message = "'%s' linked as %s translation for the current content." % (title, language)
transaction_note(message)

return state.set(portal_status_message=message)
