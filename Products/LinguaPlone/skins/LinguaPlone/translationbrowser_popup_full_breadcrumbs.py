## Script (Python) "translationbrowser_popup_full_breadcrumbs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return full breadcrumbs from portal_root til context
##
items = []
while context.portal_type != 'Plone Site':
    items.append(context)
    context = context.aq_parent

items.reverse()
return items
