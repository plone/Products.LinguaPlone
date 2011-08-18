from zope.component import adapter
from zope.event import notify
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from z3c.caching.purge import Purge

from plone.app.caching.utils import isPurged
from Products.LinguaPlone.interfaces import ITranslatable


@adapter(ITranslatable, IObjectModifiedEvent)
def purgeTranslationsOnModified(object, event):
    """ When the canonical is purged, also purge the translations. This is
        for content with language independent fields.
    """
    if isPurged(object) and object.isCanonical():
        translations = object.getTranslations(include_canonical=False)
        for translation, state in translations.values():
            notify(Purge(translation))
