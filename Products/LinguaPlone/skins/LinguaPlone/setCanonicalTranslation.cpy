##parameters=
##title=

from Products.CMFPlone.utils import transaction_note

REQUEST = context.REQUEST
putils = context.plone_utils

context.setCanonical()
for translation, ignored in context.getTranslations().values():
    translation.reindexObject()

message = context.translate(msgid='message_canonical_translation_changed',
                            default='Canonical translation changed.',
                            domain='linguaplone')
transaction_note(message)
putils.addPortalMessage(message)
return state.set()
