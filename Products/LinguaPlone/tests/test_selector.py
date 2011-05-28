# -*- coding: UTF-8 -*-

from unittest import TestCase

from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import provideAdapter
from zope.interface import directlyProvides
from zope.interface import implements
from zope.interface import Interface
from zope.testing import cleanup

from Acquisition import Explicit
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class Dummy(Explicit):

    implements(ITranslatable)

    def getTranslation(self, language='language'):
        return self.getTranslations().get(language, None)

    def getTranslations(self, review_state=False):
        return {'en': self, 'nl': self}

    def getPhysicalPath(self):
        return getattr(self, 'physicalpath', [])

    def getLanguage(self):
        return 'en'


class DummyNeutral(Explicit):

    implements(ITranslatable)

    def getTranslation(self, language='language'):
        return self.getTranslations().get(language, None)

    def getTranslations(self, review_state=False):
        return {}

    def getPhysicalPath(self):
        return getattr(self, 'physicalpath', [])

    def getLanguage(self):
        return ''


class DummyRequest(object):

    def __init__(self):
        self.form = {}

    def get(self, key, default):
        return self.__dict__.get(key, default)


class DummyState(object):

    def __init__(self, context, request):
        pass

    def canonical_object_url(self):
        return 'object_url'


class EvilObject(object):

    def __str__(self):
        raise UnicodeError

    def __unicode__(self):
        raise UnicodeError


class MockLanguageTool(object):

    use_cookie_negotiation = True

    def showSelector(self):
        return True

    def getAvailableLanguageInformation(self):
        return dict(en={'selected': True}, de={'selected': False},
                    nl={'selected': True}, no={'selected': True})

    def getLanguageBindings(self):
        # en = selected by user, nl = default, [] = other options
        return ('en', 'nl', [])

    def getSupportedLanguages(self):
        return ['nl', 'en', 'no']


class TestLanguageSelectorFindPath(cleanup.CleanUp, TestCase):

    def setUp(self):
        self.selector = TranslatableLanguageSelector(None,
                            None, None, None)
        self.fp = self.selector._findpath

    def test_findpath(self):
        result = self.fp(['', 'fake', 'path'], '/fake/path/object')
        self.assertEquals(result, ['', 'object'])

    def test_findpath_match(self):
        result = self.fp(['', 'fake', 'path'], '/fake/path')
        self.assertEquals(result, [])

    def test_findpath_match_slash(self):
        result = self.fp(['', 'fake', 'path'], '/fake/path/')
        self.assertEquals(result, [])

    def test_findpath_template(self):
        result = self.fp(['', 'fake', 'path'], '/fake/path/object/atct_edit')
        self.assertEquals(result, ['', 'object', 'atct_edit'])

    def test_findpath_view(self):
        result = self.fp(['', 'fake', 'path'], '/fake/path/object/@@sharing')
        self.assertEquals(result, ['', 'object', '@@sharing'])

    def test_findpath_vhr(self):
        result = self.fp(['', 'fake', 'path'],
            '/VirtualHostBase/http/127.0.0.1/fake/path/VirtualHostRoot/object')
        self.assertEquals(result, ['', 'object'])

    def test_findpath_vh_marker(self):
        result = self.fp(['', 'fake', 'path'],
            '/VirtualHostBase/http/127.0.0.1/fake/path//VirtualHostRoot/' +
            '_vh_secondlevel/object')
        self.assertEquals(result, ['', 'object'])

    def test_findpath_vhr_and_traverser(self):
        result = self.fp(['', 'fake', 'path'],
            '/VirtualHostBase/http/127.0.0.1/site/fake/path/++skin++theme/' +
            'VirtualHostRoot/object')
        self.assertEquals(result, ['', 'object'])


class TestLanguageSelectorFormVariables(cleanup.CleanUp, TestCase):

    def setUp(self):
        self.selector = TranslatableLanguageSelector(None,
                            None, None, None)
        self.fv = self.selector._formvariables

    def test_formvariables(self):
        form = dict(one=1, two='2')
        self.assertEquals(self.fv(form), form)

    def test_formvariables_sequences(self):
        form = dict(one=('a', ), two=['b', 2])
        self.assertEquals(self.fv(form), form)

    def test_formvariables_unicode(self):
        uni = unicode('Før', 'utf-8')
        form = dict(one=uni, two=u'foo')
        self.assertEquals(self.fv(form),
                          dict(one=uni.encode('utf-8'), two=u'foo'))

    def test_formvariables_utf8(self):
        utf8 = unicode('Før', 'utf-8').encode('utf-8')
        form = dict(one=utf8, two=u'foo')
        self.assertEquals(self.fv(form), form)

    def test_formvariables_object(self):
        form = dict(one='1', two=EvilObject())
        self.assertEquals(self.fv(form), form)


class TestLanguageSelectorBasics(cleanup.CleanUp, TestCase):

    def setUp(self):
        provideAdapter(DummyState, adapts=(Dummy, DummyRequest),
                       provides=Interface, name="plone_context_state")
        self.context = Dummy()
        self.context.portal_url = Dummy()
        self.container = Dummy()
        self.context = self.context.__of__(self.container)
        self.request = DummyRequest()
        self.selector = TranslatableLanguageSelector(self.context,
                            self.request, None, None)

    def test_available(self):
        self.selector.update()
        self.selector.tool = MockLanguageTool()
        self.assertEquals(self.selector.available(), True)

    def test_available_no_tool(self):
        self.selector.update()
        self.selector.tool = None
        self.assertEquals(self.selector.available(), False)

    def test_languages(self):
        self.selector.update()
        self.selector.tool = MockLanguageTool()
        self.assertEqual(self.selector.languages(),
            [{'code': 'nl',
              'translated': True,
              'selected': False,
              'url': 'object_url?set_language=nl'},
             {'code': 'en',
              'translated': True,
              'selected': True,
              'url': 'object_url?set_language=en'},
             {'code': 'no',
               'translated': False,
               'selected': False,
               'url': 'object_url?set_language=no'},
             ])

    def test_languages_vhr(self):
        self.context.physicalpath = ['', 'fake', 'path']
        vbase = '/VirtualHostBase/http/127.0.0.1/'
        self.request.PATH_INFO = vbase + 'fake/path/VirtualHostRoot/to/object'
        self.request.form['uni'] = u'pres\xd8rved'
        self.request.form['int'] = '1'
        self.selector.update()
        self.selector.tool = MockLanguageTool()
        base = 'object_url/to/object?int=1&uni='
        expected = [
            {'code': 'nl',
             'translated': True,
             'selected': False,
             'url': base + 'pres%C3%98rved&set_language=nl'},
            {'code': 'en',
             'translated': True,
             'selected': True,
             'url': base + 'pres%C3%98rved&set_language=en'},
            {'code': 'no',
             'translated': False,
             'selected': False,
             'url': 'object_url?int=1&uni=pres%C3%98rved&set_language=no'}]
        self.assertEqual(self.selector.languages(), expected)

    def test_languages_preserve_view_and_query(self):
        self.context.physicalpath = ['', 'fake', 'path']
        self.request.PATH_INFO = '/fake/path/to/object'
        self.selector.update()
        self.selector.tool = MockLanguageTool()
        base = 'object_url/to/object?set_language='
        expected = [
            {'code': 'nl',
             'translated': True,
             'selected': False,
             'url': base + 'nl'},
            {'code': 'en',
             'translated': True,
             'selected': True,
             'url': base + 'en'},
            {'code': 'no',
             'translated': False,
             'selected': False,
             'url': 'object_url?set_language=no'}]
        self.assertEqual(self.selector.languages(), expected)


class TestLanguageSelectorBasicsOnNeutral(cleanup.CleanUp, TestCase):

    def setUp(self):
        provideAdapter(DummyState, adapts=(DummyNeutral, DummyRequest),
                       provides=Interface, name="plone_context_state")
        self.context = DummyNeutral()
        self.context.portal_url = DummyNeutral()
        self.container = DummyNeutral()
        self.context = self.context.__of__(self.container)
        self.request = DummyRequest()
        self.selector = TranslatableLanguageSelector(self.context,
                            self.request, None, None)

    def test_languages_preserve_view_and_query(self):
        self.context.physicalpath = ['', 'fake', 'path']
        self.request.PATH_INFO = '/fake/path/to/object'
        self.selector.update()
        self.selector.tool = MockLanguageTool()
        base = 'object_url/to/object?set_language='
        expected = [
            {'code': 'nl',
             'translated': False,
             'selected': False,
             'url': base + 'nl'},
            {'code': 'en',
             'translated': False,
             'selected': True,
             'url': base + 'en'},
            {'code': 'no',
             'translated': False,
             'selected': False,
             'url': base + 'no'}]
        self.assertEqual(self.selector.languages(), expected)


class TestLanguageSelectorRendering(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('no')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')
        self.german.setLanguage('de')

    def testRenderSelectorOnContent(self):
        request = self.app.REQUEST
        selector = TranslatableLanguageSelector(
            self.english, request, None, None)
        selector.update()
        output = selector.render()
        self.assert_('<ul id="portal-languageselector"' in output)
        en_path = self.english.absolute_url()
        en_link = '<a href="%s?set_language=en"' % en_path
        self.assert_(en_link in output)
        de_path = self.german.absolute_url()
        de_link = '<a href="%s?set_language=de"' % de_path
        self.assert_(de_link in output)
        no_path = self.portal.absolute_url()
        no_link = '<a href="%s?set_language=no"' % no_path
        self.assert_(no_link in output)

    def testRenderSelectorWithView(self):
        request = self.app.REQUEST
        request['PATH_INFO'] = '@@myview'
        selector = TranslatableLanguageSelector(
            self.english, request, None, None)
        selector.update()
        output = selector.render()
        self.assert_('<ul id="portal-languageselector"' in output)
        en_path = self.english.absolute_url() + '/@@myview'
        en_link = '<a href="%s?set_language=en"' % en_path
        self.assert_(en_link in output)
        de_path = self.german.absolute_url() + '/@@myview'
        de_link = '<a href="%s?set_language=de"' % de_path
        self.assert_(de_link in output)
        no_path = self.portal.absolute_url()
        no_link = '<a href="%s?set_language=no"' % no_path
        self.assert_(no_link in output)

    def testRenderSelectorOnSiteRoot(self):
        request = self.app.REQUEST
        selector = TranslatableLanguageSelector(
            self.portal, request, None, None)
        selector.update()
        output = selector.render()
        path = self.portal.absolute_url()
        de_link = '<a href="%s?set_language=de"' % path
        self.assert_(de_link in output)
        en_link = '<a href="%s?set_language=en"' % path
        self.assert_(en_link in output)

    def testRenderSelectorWithNavigationRoot(self):
        request = self.app.REQUEST
        directlyProvides(self.portal.Members, INavigationRoot)
        selector = TranslatableLanguageSelector(
            self.folder, request, None, None)
        selector.update()
        output = selector.render()
        path = self.portal.Members.absolute_url()
        folder_path = self.folder.absolute_url()
        de_link = '<a href="%s?set_language=de"' % path
        self.assert_(de_link in output)
        en_link = '<a href="%s?set_language=en"' % folder_path
        self.assert_(en_link in output)

    def testRenderSelectorWithFlags(self):
        request = self.app.REQUEST
        ltool = getToolByName(self.portal, 'portal_languages')
        ltool.display_flags = True
        selector = TranslatableLanguageSelector(
            self.english, request, None, None)
        selector.update()
        output = selector.render()
        self.assert_('de.gif' in output)
        self.assert_('gb.gif' in output)

    def testRenderSelectorWithoutCookieNegotiation(self):
        request = self.app.REQUEST
        ltool = getToolByName(self.portal, 'portal_languages')
        ltool.use_cookie_negotiation = False
        selector = TranslatableLanguageSelector(
            self.english, request, None, None)
        selector.update()
        output = selector.render()
        self.assertEquals(output.strip(), u'')
