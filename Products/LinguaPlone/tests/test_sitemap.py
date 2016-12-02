# -*- coding: utf-8 -*-
from gzip import GzipFile
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation
from StringIO import StringIO

import unittest

# For Fixture class below
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

# This class and its instantions probably should be moved to a testing.py file
class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.LinguaPlone
        self.loadZCML(package=Products.LinguaPlone)

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='Products.LinguaPlone:Integration',
)


# This class largely inspired by plone/app/layout/sitemap/tests/test_sitemap.py
class TestSitemap(unittest.TestCase):
    
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        self.portal.portal_languages.addSupportedLanguage('ca')
        self.portal.portal_languages.addSupportedLanguage('es')
        en = makeContent(self.portal, 'Folder', id='en')
        en.setLanguage('en')

        self.ca_folder = en.addTranslation('ca')
        alsoProvides(self.ca_folder, INavigationRoot)

        self.es_folder = en.addTranslation('es')
        alsoProvides(self.es_folder, INavigationRoot)

        self.sitemap = getMultiAdapter((self.portal, self.portal.REQUEST),
                                       name='sitemap.xml.gz')
        self.site_properties = getToolByName(
            self.portal, 'portal_properties').site_properties
        self.site_properties.manage_changeProperties(enable_sitemap=True)
        doc_ca = makeContent(
            self.ca_folder,
            'Document',
            title=u'Test document',
            id='test-document')
        doc_es = makeContent(
            self.es_folder,
            'Document',
            title=u'Test document',
            id='test-document')
        doc_en = makeContent(
            self.portal['en'],
            'Document',
            title=u'Test document',
            id='test-document')
        doc_ca.setLanguage('ca')
        doc_es.setLanguage('es')
        doc_en.setLanguage('en')

    def uncompress(self, sitemapdata):
        sio = StringIO(sitemapdata)
        unziped = GzipFile(fileobj=sio)
        xml = unziped.read()
        unziped.close()
        return xml

    def test_portalroot_sitemap(self):
        '''
        Requests for the sitemap on portalroot return all languages
        '''
        xml = self.uncompress(self.sitemap())
        self.assertIn(
            '<loc>http://nohost/plone/%s/test-document</loc>' % self.ca_folder.id,
             xml)
        self.assertIn(
            '<loc>http://nohost/plone/en/test-document</loc>',
             xml)
        self.assertIn(
            '<loc>http://nohost/plone/%s/test-document</loc>' % self.es_folder.id,
             xml)

    def test_navroot_sitemap(self):
        '''
        Sitemap generated from a LanguageRootFolder (an INavigationRoot)
        '''
        sitemap = getMultiAdapter(
            (self.es_folder, self.portal.REQUEST), name='sitemap.xml.gz')
        xml = self.uncompress(sitemap())
        self.assertNotIn(
            '<loc>http://nohost/plone/%s/test-document</loc>' % self.ca_folder.id,
            xml)
        self.assertNotIn(
            '<loc>http://nohost/plone/en/test-document</loc>',
            xml)
        self.assertIn(
            '<loc>http://nohost/plone/%s/test-document</loc>' % self.es_folder.id,
            xml)
