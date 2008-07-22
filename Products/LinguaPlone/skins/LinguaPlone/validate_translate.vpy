## Script (Python) "validate_base"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=lp_translating_from, lp_translating_to
##
errors = {}

if lp_translating_from == lp_translating_to:
    message = context.translate(msgid='message_select_different_languages',
                                default='Please select different values '
                                        'for each language.',
                                domain='linguaplone')
    return state.set(status='failure', errors=errors,
                     portal_status_message=message)

errors = context.validate(REQUEST=context.REQUEST, errors=errors, data=1, metadata=0)

if errors:
    return state.set(status='failure', errors=errors,
                     portal_status_message='Please correct the indicated errors.')
else:
    return state.set(portal_status_message='Your changes have been saved.')
