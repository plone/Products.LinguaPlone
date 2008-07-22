from Products.CMFCore.utils import getToolByName

def importVarious(context):
    if context.readDataFile("linguaplone-various.txt") is None:
        return

    site=context.getSite()

    qi = getToolByName(site, 'portal_quickinstaller', None)
    if not qi.isProductInstalled('PloneLanguageTool'):
        setup = getToolByName(site, 'portal_setup')
        old_context = setup.getImportContextID()
        qi.installProduct('PloneLanguageTool')
        # This is deprecated but makes nested imports work
        setup.setImportContext(old_context)

