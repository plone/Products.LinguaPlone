##parameters=languages=None
##title=

from Products.CMFPlone.utils import transaction_note
from Products.CMFPlone.utils import safe_unicode

REQUEST = context.REQUEST
titles = []
titles_and_ids = []

if languages is None:
    languages = []

status = 'success_translate'
message = "Please select one or more items to delete."

if context.getLanguage() in languages:
    # We are deleting the current object. Redirect to the 
    # canonical translation instead.
    o = context.getCanonical()
    if o is None:
        raise Exception, "Canonical translation object not found"
else:
    o = context

for language in languages:
    obj = context.getTranslation(language)
    title_or_id = safe_unicode(obj.title_or_id())
    titles.append(title_or_id)
    titles_and_ids.append('%s (%s)' % (title_or_id, obj.getId()))
    context.removeTranslation(language)

if languages:
    transaction_note('Deleted translation(s) %s' % (', '.join(titles_and_ids),))
    message = '%s has been deleted.' % (', '.join(titles),)

context.plone_utils.addPortalMessage(message)
return state.set(context=o, status=status)
