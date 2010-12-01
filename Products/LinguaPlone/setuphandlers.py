from Products.CMFCore.utils import getToolByName


def importReindexLanguageIndex(context):
    if context.readDataFile("linguaplone-reindex.txt") is None:
        return
    site = context.getSite()
    logger = context.getLogger('LinguaPlone')

    # Recent GS versions have import steps on the tool, older versions
    # need to check the registry.
    tool = context.getSetupTool()
    registry = tool.getImportStepRegistry()    
    checkmethod = getattr(tool, 'getImportStep', None) or \
                  getattr(tool.getImportStepRegistry(), 'getStep')    
    if checkmethod('browserlayer') is None:
        msg="Can not install LinguaPlone: you need to install 'Local " \
            "browser layer support' from plone.browserlayer first."
        logger.error(msg)
        raise RuntimeError, msg

    catalog = getToolByName(site, 'portal_catalog')

    if 'Language' in catalog.indexes():
        index = catalog._catalog.getIndex('Language')
        # We do not want a FieldIndex but a LanguageIndex
        if index.meta_type != 'LanguageIndex':
            catalog.delIndex('Language')

    # Check again.
    if 'Language' not in catalog.indexes():
        catalog.addIndex('Language', 'LanguageIndex')
        logger.info("Added LanguageIndex field Language.")

    # Reindex when there are no objects.
    index = catalog._catalog.getIndex('Language')
    if index.numObjects() == 0:
        catalog.reindexIndex('Language', None)
