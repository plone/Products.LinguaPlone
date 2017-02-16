from Products.CMFCore.utils import getToolByName


def importReindexLanguageIndex(context):
    if context.readDataFile("linguaplone-reindex.txt") is None:
        return
    site = context.getSite()
    logger = context.getLogger('LinguaPlone')
    catalog = getToolByName(site, 'portal_catalog')

    if 'Language' in catalog.indexes():
        index = catalog._catalog.getIndex('Language')
        # We do not want a LanguageIndex but a FieldIndex
        if index.meta_type != 'FieldIndex':
            catalog.delIndex('Language')

    # Check again.
    if 'Language' not in catalog.indexes():
        extra = {'indexed_attrs': ['Language']}
        catalog.addIndex('Language', 'FieldIndex', extra)
        logger.info("Added FieldIndex for field Language.")

    # Reindex when there are no objects.
    index = catalog._catalog.getIndex('Language')
    if index.numObjects() == 0:
        catalog.reindexIndex('Language', None)


def uninstall(context):
    if context.readDataFile("linguaplone-uninstall.txt") is None:
        return
    site = context.getSite()
    logger = context.getLogger('LinguaPlone')
    qi = getToolByName(site, 'portal_quickinstaller')
    try:
        qi.uninstallProducts(products=['LinguaPlone'])
    except AttributeError:
        # Already uninstalled. Don't fail.
        pass
    o = qi._getOb('LinguaPlone', None)
    if o:
        assert(not o.isInstalled())
    logger.info('Uninstalled LinguaPlone from portal_quickinstaller.')
