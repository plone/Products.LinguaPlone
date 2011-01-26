from zope.component import getSiteManager

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.tests.base import LinguaPloneTestCase


class TestUpgrades(LinguaPloneTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addLanguage('de')
        self.addLanguage('no')
        self.gs = getToolByName(self.portal, 'portal_setup')

    def test_remove_old_import_step(self):
        from ..upgrades import remove_old_import_step
        registry = self.gs.getImportStepRegistry()
        step = u'linguaplone_various'
        # add step back
        registry.registerStep(step, handler='a.b', title='', description='')
        self.assert_(step in registry.listSteps())
        for i in range(2):
            remove_old_import_step(self.gs)
        self.assert_(step not in registry.listSteps())

    def test_add_language_metadata(self):
        from ..upgrades import add_language_metadata
        tool = getToolByName(self.portal, 'reference_catalog')
        tool.delColumn('Language')
        self.assert_('Language' not in tool.schema())
        for i in range(2):
            add_language_metadata(self.gs)
        self.assert_('Language' in tool.schema())

    def test_add_uid_language_index(self):
        from ..upgrades import add_uid_language_index
        tool = getToolByName(self.portal, 'uid_catalog')
        tool.delIndex('Language')
        self.assert_('Language' not in tool.indexes())
        for i in range(2):
            add_uid_language_index(self.gs)
        self.assert_('Language' in tool.indexes())
        index = tool._catalog.getIndex('Language')
        self.assert_(index.numObjects() > 0)

    def test_add_synced_vocabularies(self):
        from ..upgrades import add_synced_vocabularies
        from plone.i18n.locales.interfaces import IContentLanguageAvailability
        from plone.i18n.locales.interfaces import IMetadataLanguageAvailability
        from plone.app.i18n.locales.languages import ContentLanguages
        from plone.app.i18n.locales.languages import MetadataLanguages
        from Products.LinguaPlone.vocabulary import SyncedLanguages
        site = getSiteManager(context=self.gs)
        # register different type of utilities
        util1 = site.queryUtility(IContentLanguageAvailability)
        site.unregisterUtility(component=aq_base(util1),
            provided=IContentLanguageAvailability)
        site.registerUtility(component=ContentLanguages(),
            provided=IContentLanguageAvailability)
        util2 = site.queryUtility(IMetadataLanguageAvailability)
        site.unregisterUtility(component=aq_base(util2),
            provided=IMetadataLanguageAvailability)
        site.registerUtility(component=MetadataLanguages(),
            provided=IMetadataLanguageAvailability)
        util1 = site.queryUtility(IContentLanguageAvailability)
        self.assertEquals(type(aq_base(util1)), ContentLanguages)
        util2 = site.queryUtility(IMetadataLanguageAvailability)
        self.assertEquals(type(aq_base(util2)), MetadataLanguages)
        for i in range(2):
            add_synced_vocabularies(self.gs)
        util1 = site.queryUtility(IContentLanguageAvailability)
        self.assertEquals(type(aq_base(util1)), SyncedLanguages)
        util2 = site.queryUtility(IMetadataLanguageAvailability)
        self.assertEquals(type(aq_base(util2)), SyncedLanguages)

    def test_add_properties_sheet(self):
        from ..upgrades import add_properties_sheet
        tool = getToolByName(self.portal, 'portal_properties')
        del tool['linguaplone_properties']
        self.assert_('linguaplone_properties' not in tool)
        for i in range(2):
            add_properties_sheet(self.gs)
        self.assert_('linguaplone_properties' in tool)
        props = tool.linguaplone_properties
        key = 'hide_right_column_on_translate_form'
        self.assertEquals(props.getProperty(key), True)
