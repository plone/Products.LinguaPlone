from zope.interface import implementer
from zope.site.hooks import getSite

from plone.i18n.locales.interfaces import IContentLanguageAvailability
from plone.i18n.locales.interfaces import IMetadataLanguageAvailability
from plone.i18n.locales.languages import LanguageAvailability


@implementer(IContentLanguageAvailability, IMetadataLanguageAvailability)
class SyncedLanguages(LanguageAvailability):

    def getAvailableLanguages(self, combined=False):
        """Return a sequence of language tags for available languages.
        """
        langs = LanguageAvailability.getAvailableLanguages(self,
                                                           combined=combined)
        # Filter languages to the supported ones
        site = getSite()
        langtool = getattr(site, 'portal_languages', None)
        if langtool is not None:
            supported = [unicode(l) for l in langtool.getSupportedLanguages()]
            # We have a list of languages codes
            langs = [l for l in langs if l in supported]
        return langs

    def getLanguages(self, combined=False):
        """Return a sequence of Language objects for available languages.
        """
        langs = LanguageAvailability.getLanguages(self, combined=combined)
        # Filter languages to the supported ones
        site = getSite()
        langtool = getattr(site, 'portal_languages', None)
        if langtool is not None:
            supported = [unicode(l) for l in langtool.getSupportedLanguages()]
            # We have a dictonary of dictonaries, keyed by language code
            new_langs = dict()
            for s in supported:
                new_langs[s] = langs[s]
            langs = new_langs
        return langs

    def getLanguageListing(self, combined=False):
        """Return a sequence of language code and language name tuples.
        """
        langs = LanguageAvailability.getLanguageListing(self,
                                                        combined=combined)
        # Filter languages to the supported ones
        site = getSite()
        langtool = getattr(site, 'portal_languages', None)
        if langtool is not None:
            supported = [unicode(l) for l in langtool.getSupportedLanguages()]
            # We have a list of tuples (code, name)
            langs = [l for l in langs if l[0] in supported]
        return langs

synced = SyncedLanguages()
