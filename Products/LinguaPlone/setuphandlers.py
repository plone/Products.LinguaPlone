from Products.CMFCore.utils import getToolByName

def importVarious(context):
    if context.readDataFile("linguaplone-various.txt") is None:
        return

    site=context.getSite()

    catalog=getToolByName(site, 'portal_catalog')
    index=catalog._catalog.getIndex("Language")
    if index.numObjects()==0:
        catalog.reindexIndex('Language', None)


