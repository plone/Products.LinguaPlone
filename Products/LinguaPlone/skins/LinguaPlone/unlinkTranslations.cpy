##parameters=languages=[]
##title=

from Products.CMFPlone.utils import transaction_note
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
    titles.append(obj.title_or_id())
    titles_and_ids.append('%s (%s)' % (obj.title_or_id(), obj.getId()))
    context.removeTranslationReference(obj)

status = 'success_translate'

if languages:
    transaction_note('Unlinked translation(s) %s' % (', '.join(titles_and_ids),))
    message = '%s has been deleted.' % (', '.join(titles),)
else:
    message = "Please select one or more items to delete."


return state.set(context=o, status=status, portal_status_message=message)
