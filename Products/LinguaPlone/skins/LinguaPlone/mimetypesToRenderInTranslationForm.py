## Script (Python) "mimetypesToRenderInTranslationForm"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# return a list of mime-types that should be rendered
# ie: that we call the acessor instead of the editaccessor
# when displaying as canonical for the translationform
#
# By default used to handle stuff that is text/html for
# use with the richwidget

return ('text/html', 'text/x-rst')
