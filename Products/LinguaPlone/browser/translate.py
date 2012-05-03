from zope.component import getMultiAdapter, getGlobalSiteManager
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from Products.LinguaPlone import LinguaPloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone.i18n.locales.interfaces import ILanguageAvailability


class CreateTranslation(BrowserView):

    def _setCanonicalLanguage(self, obj):
        """Make sure an object has a language set (ie is not neutral).
        """
        lang=obj.Language()
        if not lang:
            portal_state=getMultiAdapter((self.context, self.request),
                                    name="plone_portal_state")
            lang=portal_state.language()
            obj.setLanguage(lang)

    def nextUrl(self, trans):
        """Figure out where users should go after creating the translation.
        """
        fti = trans.getTypeInfo()
        try:
            return fti.getActionInfo("object/translate", object=trans)['url']
        except ValueError:
            pass

        try:
            return fti.getActionInfo("object/edit", object=trans)['url']
        except ValueError:
            pass

        state = getMultiAdapter(
            (trans, self.request), name="plone_context_state")
        return state.view_url()

    def __call__(self):
        status = IStatusMessage(self.request)
        self._setCanonicalLanguage(self.context)

        newlang=self.request["newlanguage"]

        lt=getToolByName(self.context, "portal_languages")
        lt.setLanguageCookie(newlang)

        if self.context.hasTranslation(newlang):
            status.addStatusMessage(_(u"message_translation_exists",
                                        default=u"Translation already exists"),
                                    type="info")
        else:
            self.context.addTranslation(newlang)
            status.addStatusMessage(_(u"message_translation_created",
                                      default=u"Translation created."),
                                    type="info")
        trans = self.context.getTranslation(newlang)

        return self.request.response.redirect(self.nextUrl(trans))


class TranslationHelpers(BrowserView):

    def getUntranslatedLanguages(self):
        lt = getToolByName(self.context, "portal_languages")
        languages = lt.listSupportedLanguages()
        translated = self.context.getTranslationLanguages()
        languages = [lang for lang in languages if lang[0] not in translated]
        languages.sort(key=lambda x: x[1])
        return languages

    def getDeletableLanguages(self):
        context = self.context
        lt = getToolByName(context, 'portal_languages')
        gsm = getGlobalSiteManager()
        util = gsm.queryUtility(ILanguageAvailability)
        if lt.use_combined_language_codes:
            lang_names = dict(util.getLanguageListing(combined=True))
        else:
            lang_names = dict(util.getLanguageListing())
        translations = context.getTranslations(
            include_canonical=False, review_state=False)

        # Return dictionary of information about existing translations
        # tuples of lang id, lang name and content title
        languages = []
        for lang, item in translations.items():
            languages.append(dict(id=lang, name=lang_names.get(lang, lang),
                title = safe_unicode(item.Title()),
                path = item.absolute_url_path()))

        def lcmp(x, y):
            return cmp(x['name'], y['name'])

        languages.sort(lcmp)
        return languages

    def getTranslatedLanguages(self):
        context = self.context
        allLanguages = context.portal_languages.listSupportedLanguages()
        translated = context.getTranslationLanguages()

        # Only return available translations if they are in the allowed langs from languageTool
        languages = [lang for lang in allLanguages if lang[0] in translated]

        def lcmp(x, y):
            return cmp(x[1], y[1])

        languages.sort(lcmp)
        return languages
