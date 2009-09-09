from zope.interface import implements
from zope.component import provideAdapter
from zope.interface import Interface
from zope.testing import cleanup
from unittest import TestCase
from Acquisition import Explicit
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable

class Dummy(Explicit):
    implements(ITranslatable)

    def objectIds(self):
        return ()

    def getPortalObject(self):
        return self

    def absolute_url(self):
        return 'absolute url'

    def getTranslations(self):
        return {'en':[self, 'published'],
                'nl':[self, 'published']}

    def getPhysicalPath(self):
        return getattr(self, 'physicalpath', [])


class DummyRequest(object):
    def get(self, key, default):
        return self.__dict__.get(key, default)
    form = {}


class DummyState(object):
    def __init__(self, context, request):
        pass

    def view_url(self):
        return 'view_url'


class MockLanguageTool(object):
    use_cookie_negotiation = True

    def showFlags(self):
        return True

    def getAvailableLanguageInformation(self):
        return dict(en={'selected' : True}, de={'selected' : False},
                    nl={'selected' : True})

    def getLanguageBindings(self):
        # en = selected by user, nl = default, [] = other options
        return ('en', 'nl', [])

    def getSupportedLanguages(self):
        return ['nl', 'en']


class TestLanguageSelector(cleanup.CleanUp, TestCase):
    def setUp(self):
        provideAdapter(DummyState, adapts=(Dummy, DummyRequest),
                       provides=Interface, name="plone_context_state")
        self.context=Dummy()
        self.context.portal_url = Dummy()
        self.container=Dummy()
        self.context = self.context.__of__(self.container)
        self.request=DummyRequest()
        self.selector=TranslatableLanguageSelector(self.context,
                        self.request, None, None)


    def testLanguages(self):
        self.selector.update()
        self.selector.tool=MockLanguageTool()
        self.assertEqual(self.selector.languages(),
                [ {'code': 'nl',
                   'translated': True,
                   'selected': False,
                   'url': 'view_url?set_language=nl',
                   },
                   {'code': 'en',
                    'translated': True,
                    'selected': True,
                    'url': 'view_url?set_language=en',
                   },
                   ])

    def testPreserveViewAndQuery(self):
        self.context.physicalpath = ['','fake', 'path']
        self.request.PATH_INFO = '/fake/path/to/object'
        self.request.form['variable'] = u'pres\xd8rved'
        self.selector.update()
        self.selector.tool=MockLanguageTool()
        expected = \
                [ {'code': 'nl',
                   'translated': True,
                   'selected': False,
                   'url': 'view_url/to/object?variable=pres%C3%98rved&set_language=nl',
                   },
                   {'code': 'en',
                    'translated': True,
                    'selected': True,
                    'url': 'view_url/to/object?variable=pres%C3%98rved&set_language=en',
                   },
                   ]
        self.assertEqual(self.selector.languages(),expected)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLanguageSelector))
    return suite
