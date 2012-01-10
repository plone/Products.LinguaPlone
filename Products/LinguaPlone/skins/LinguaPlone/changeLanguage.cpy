##parameters=language=None
##title=

from Products.CMFPlone.utils import transaction_note
REQUEST = context.REQUEST

context.setLanguage(language)
if not language:
    language = context.translate(msgid='label_neutral',
                                 default='Neutral',
                                 domain='linguaplone')
message = context.translate(msgid='message_content_changed_language_to',
                            default='Changed content language to ${language}.',
                            mapping={'language': language},
                            domain='linguaplone')
transaction_note(message)
context.plone_utils.addPortalMessage(message)
return state.set()
