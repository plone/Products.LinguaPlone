##parameters=languages=[]
##title=

from Products.CMFPlone.utils import transaction_note
from Products.CMFPlone.utils import safe_unicode

REQUEST = context.REQUEST

if context.getLanguage() in languages:
    # We are unlinking the current object. Redirect to the
    # canonical translation instead.
    o = context.getCanonical()
    if o is None:
        raise Exception, "Canonical translation object not found"
else:
    o = context

titles = []
titles_and_ids = []

for language in languages:
    obj = context.getTranslation(language)
    title_or_id = safe_unicode(obj.title_or_id())
    titles.append(title_or_id)
    titles_and_ids.append('%s (%s)' % (title_or_id, obj.getId()))
    o.removeTranslationReference(obj)

status = 'success_translate'

if languages:
    transaction_note('Unlinked translation(s) %s' % (', '.join(titles_and_ids),))
    message = '%s has been unlinked.' % (', '.join(titles),)
else:
    message = "Please select one or more items to unlink."


context.plone_utils.addPortalMessage(message)
return state.set(context=o, status=status)
