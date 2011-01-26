from Products.LinguaPlone.catalog import languageFilter
from Products.LinguaPlone.config import I18NAWARE_CATALOG
from Products.LinguaPlone.config import NOFILTERKEYS
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestLanguageFilter(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')

    def testNoI18NAwareCatalog(self):
        original = bool(I18NAWARE_CATALOG)
        try:
            languageFilter.func_globals['I18NAWARE_CATALOG'] = False
            query = {'Language': 'all'}
            languageFilter(query)
            self.failUnless('Language' in query)
        finally:
            languageFilter.func_globals['I18NAWARE_CATALOG'] = original

    def testNoTool(self):
        self.loginAsPortalOwner()
        del self.portal['portal_languages']
        query = {'Language': 'all'}
        languageFilter(query)
        self.failUnless('Language' in query)

    def testEnglish(self):
        query = {'review_state': 'published'}
        languageFilter(query)
        self.failUnless('Language' in query)
        self.assertEquals(query['Language'], ['en', ''])

    def testGerman(self):
        query = {'review_state': 'published', 'Language': 'de'}
        languageFilter(query)
        self.failUnless('Language' in query)
        self.assertEquals(query['Language'], 'de')

    def testMultiple(self):
        query = {'review_state': 'published', 'Language': ['en', 'de']}
        languageFilter(query)
        self.failUnless('Language' in query)
        self.assertEquals(query['Language'], ['en', 'de'])

    def testNeutral(self):
        query = {'review_state': 'published', 'Language': ''}
        languageFilter(query)
        self.failUnless('Language' in query)
        self.assertEquals(query['Language'], '')

    def testAll(self):
        query = {'review_state': 'published', 'Language': 'all'}
        languageFilter(query)
        self.failIf('Language' in query)

    def testNoFilter(self):
        self.failUnless('UID' in NOFILTERKEYS)
        query = {'UID': '123'}
        languageFilter(query)
        self.failIf('Language' in query)

    def testNoFilterExplicitLanguage(self):
        self.failUnless('UID' in NOFILTERKEYS)
        query = {'UID': '123', 'Language': 'de'}
        languageFilter(query)
        self.failUnless('Language' in query)
        self.assertEquals(query['Language'], 'de')


class TestMultilingualCatalog(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.edit(title='Foo', language='en')
        self.german = makeTranslation(self.english, 'de')
        self.german.edit(title='Foo')
        self.catalog = self.portal.portal_catalog

    def testSearchEnglish(self):
        search = self.catalog(Language='en')
        self.failUnless(self.english in [x.getObject() for x in search])
        self.failIf(self.german in [x.getObject() for x in search])

    def testSearchGerman(self):
        search = self.catalog(Language='de')
        self.failIf(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])

    def testSearchAllWithRequest(self):
        search = self.catalog(REQUEST = {}, Language='all')
        self.failUnless(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])

    def testSearchAll(self):
        search = self.catalog(Language='all')
        self.failUnless(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])

    def testSearchTitleEnglish(self):
        search = self.catalog(Title='Foo')
        self.failUnless(self.english in [x.getObject() for x in search])
        self.failIf(self.german in [x.getObject() for x in search])

    def testSearchTitleGerman(self):
        self.setLanguage('de')
        search = self.catalog(Title='Foo')
        self.failIf(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])

    def testSearchAllAndTitle(self):
        search = self.catalog(Language='all', Title='Foo')
        self.failUnless(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])

    def testSearchAllAndBadTitle(self):
        search = self.catalog(Language='all', Title='Bar')
        self.failIf(self.english in [x.getObject() for x in search])
        self.failIf(self.german in [x.getObject() for x in search])

    def testSearchGermanAndTitle(self):
        search = self.catalog(Language='de', Title='Foo')
        self.failIf(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])

    def testMultipleLanguages(self):
        search = self.catalog(Language=['en', 'de'])
        self.failUnless(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])

    def testMultipleLanguagesAndTitle(self):
        search = self.catalog(Language=['en', 'de'], Title='Foo')
        self.failUnless(self.english in [x.getObject() for x in search])
        self.failUnless(self.german in [x.getObject() for x in search])
