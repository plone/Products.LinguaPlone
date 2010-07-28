import logging

from plone.i18n.locales.interfaces import IContentLanguageAvailability
from plone.i18n.locales.interfaces import IMetadataLanguageAvailability
from plone.app.i18n.locales.languages import ContentLanguages
from plone.app.i18n.locales.languages import MetadataLanguages
from zope.component import getSiteManager

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.vocabulary import SyncedLanguages


def remove_old_import_step(context):
    # context is portal_setup which is nice
    registry = context.getImportStepRegistry()
    old_step = u'linguaplone_various'
    if old_step in registry.listSteps():
        registry.unregisterStep(old_step)

        # Unfortunately we manually have to signal the context
        # (portal_setup) that it has changed otherwise this change is
        # not persisted.
        context._p_changed = True
        log = logging.getLogger("LinguaPlone")
        log.info("Old %s import step removed from import registry.", old_step)


def add_language_metadata(context):
    log = logging.getLogger("LinguaPlone")
    tool = getToolByName(context, 'reference_catalog')
    if 'Language' not in tool.schema()[:]:
        tool.addColumn('Language')
        log.info("Added Language to the reference catalog metadata.")
        log.info("Updating reference catalog...")
        tool.refreshCatalog()
        log.info("Reference catalog updated.")


def add_uid_language_index(context):
    log = logging.getLogger("LinguaPlone")
    tool = getToolByName(context, 'uid_catalog')
    if 'Language' not in tool.indexes():
        tool.addIndex('Language', 'FieldIndex')
        log.info("Added FieldIndex for field Language.")
        # Reindex when there are no objects.
        index = tool._catalog.getIndex('Language')
        if index.numObjects() == 0:
            log.info("Updating UID catalog...")
            tool.reindexIndex('Language', None)
            log.info("UID catalog updated.")


def add_synced_vocabularies(context):
    log = logging.getLogger("LinguaPlone")
    site = getSiteManager(context=context)

    util = site.queryUtility(IContentLanguageAvailability)
    if util is not None:
        if not isinstance(util, SyncedLanguages):
            if isinstance(aq_base(util), ContentLanguages):
                site.unregisterUtility(component=aq_base(util),
                    provided=IContentLanguageAvailability)
                del util
                site.registerUtility(component=SyncedLanguages(),
                    provided=IContentLanguageAvailability)
                log.info("Converted content language vocabulary.")

    util = site.queryUtility(IMetadataLanguageAvailability)
    if util is not None:
        if not isinstance(util, SyncedLanguages):
            if isinstance(aq_base(util), MetadataLanguages):
                site.unregisterUtility(component=aq_base(util),
                    provided=IMetadataLanguageAvailability)
                del util
                site.registerUtility(component=SyncedLanguages(),
                    provided=IMetadataLanguageAvailability)
                log.info("Converted metadata language vocabulary.")


def add_properties_sheet(context):
    context.runImportStepFromProfile(
        'profile-Products.LinguaPlone:LinguaPlone',
        'propertiestool',
        run_dependencies=False,
        purge_old=False)
