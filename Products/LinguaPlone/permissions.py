from Products.CMFCore import permissions

View = permissions.View
AddPortalContent = permissions.AddPortalContent
ModifyPortalContent = permissions.ModifyPortalContent
AccessContentsInformation = permissions.AccessContentsInformation

AddLanguageIndex = 'LinguaPlone: Add LanguageIndex'
permissions.setDefaultRoles(AddLanguageIndex, ('Manager', ))

del permissions
