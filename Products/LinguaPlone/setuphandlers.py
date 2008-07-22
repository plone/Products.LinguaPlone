from Products.CMFCore.utils import getToolByName
import logging

def importVarious(context):
    if context.readDataFile("linguaplone-various.txt") is None:
        return

    site=context.getSite()

    qi=getToolByName(site, 'portal_quickinstaller')
    if not qi.isProductInstalled("plone.browserlayer"):
        logger=logging.getLogger("plone")
        msg="Can not install LinguaPlone: you need to install 'Local " \
            "browser layer support' from plone.browserlayer first."
        logger.error(msg)
        raise RuntimeError, msg

    catalog=getToolByName(site, 'portal_catalog')
    index=catalog._catalog.getIndex("Language")
    if index.numObjects()==0:
        catalog.reindexIndex('Language', None)


