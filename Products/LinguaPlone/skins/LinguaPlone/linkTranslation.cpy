##parameters=link_language=None,link_content=None
##title=

from Products.CMFPlone.utils import transaction_note
from Products.CMFPlone.utils import safe_unicode

REQUEST = context.REQUEST

if link_content in (None, ''):
    message = context.translate(msgid='message_content_not_found',
                                default="Translation content not found.",
                                domain='linguaplone')
    context.plone_utils.addPortalMessage(message, 'error')
    return state.set(status='failure')

translation = context.reference_catalog.lookupObject(link_content)

if translation is None:
    message = context.translate(msgid='message_content_not_found',
                                default="Translation content not found.",
                                domain='linguaplone')
    context.plone_utils.addPortalMessage(message, 'error')
    return state.set(status='failure')

if link_language not in context.portal_languages.getSupportedLanguages():
    message = context.translate(msgid='message_invalid_language',
                                default="Invalid language.",
                                domain='linguaplone')
    context.plone_utils.addPortalMessage(message, 'error')
    return state.set(status='failure')

# Unlink from current translations
translation.setLanguage('')

# Set new language, and link to current object
translation.setLanguage(link_language)
canonical = context.getCanonical()
translation.addTranslationReference(canonical)

title = safe_unicode(translation.Title())
language = context.portal_languages.getNameForLanguageCode(link_language)

message = "'%s' linked as %s translation for the current content." % (title, language)
transaction_note(message)

context.plone_utils.addPortalMessage(message)
return state.set()
