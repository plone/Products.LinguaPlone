from Products.CMFCore.utils import getToolByName
import logging

def importReindexLanguageIndex(context):
    if context.readDataFile("linguaplone-reindex.txt") is None:
        return
    site=context.getSite()
    catalog=getToolByName(site, 'portal_catalog')
    index=catalog._catalog.getIndex("Language")
    if index.numObjects()==0:
        catalog.reindexIndex('Language', None)

    # recent GS version have it on the tool, older need to check the registry
    tool = context.getSetupTool()
    registry = tool.getImportStepRegistry()    
    checkmethod = getattr(tool, 'getImportStep', None) or \
                  getattr(tool.getImportStepRegistry(), 'getStep')    
    if checkmethod('browserlayer') is None:
        logger=logging.getLogger("plone")
        msg="Can not install LinguaPlone: you need to install 'Local " \
            "browser layer support' from plone.browserlayer first."
        logger.error(msg)
        raise RuntimeError, msg