from zope.component import adapter, getGlobalSiteManager
from zope.lifecycleevent import ObjectModifiedEvent

from zope.event import notify

from z3c.caching.interfaces import IPurgeEvent

from Products.LinguaPlone.interfaces import ITranslatable
from Products.LinguaPlone.tests.base import LinguaPloneTestCase

events = []


@adapter(ITranslatable, IPurgeEvent)
def gotPurged(object, event):
    events.append((object, event,))


class TestCachingSubscriber(LinguaPloneTestCase):

    def afterSetUp(self):
        gsm = getGlobalSiteManager()
        gsm.registerHandler(gotPurged)
        events[:] = []

        def isPurged(obj):
            return True

        import Products.LinguaPlone
        self._old_isPurged = Products.LinguaPlone.caching.isPurged
        Products.LinguaPlone.caching.isPurged = isPurged

    def beforeTearDown(self):
        gsm = getGlobalSiteManager()
        gsm.unregisterHandler(gotPurged)
        import Products.LinguaPlone
        Products.LinguaPlone.caching.isPurged = self._old_isPurged

    def test_caching_subscriber_with_translation(self):
        self.folder.invokeFactory('Document', id='fred')
        fred = self.folder.fred
        fred_no = fred.addTranslation('no')
        notify(ObjectModifiedEvent(fred_no))
        self.assertEqual(events, [])

    def test_caching_subscriber_with_canonical(self):
        self.folder.invokeFactory('Document', id='fred')
        fred = self.folder.fred
        fred_no = fred.addTranslation('no')
        notify(ObjectModifiedEvent(fred))
        self.assertEqual(len(events), 1)
        obj, event = events[0]
        self.assertEqual(obj, fred_no)
