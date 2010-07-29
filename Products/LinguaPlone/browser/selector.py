from plone.app.i18n.locales.browser.selector import LanguageSelector
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import getMultiAdapter

from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from ZTUtils import make_query

from Products.LinguaPlone.interfaces import ITranslatable


class TranslatableLanguageSelector(LanguageSelector):
    """Language selector for translatable content.
    """

    render = ZopeTwoPageTemplateFile('selector.pt')

    def available(self):
        if self.tool is not None:
            selector = self.tool.showSelector()
            languages = len(self.tool.getSupportedLanguages()) > 1
            return selector and languages
        return False

    def _translations(self, missing):
        # Figure out the "closest" translation in the parent chain of the
        # context. We stop at both an INavigationRoot or an ISiteRoot to look
        # for translations.
        context = aq_inner(self.context)
        translations = {}
        chain = aq_chain(context)
        for item in chain:
            if ISiteRoot.providedBy(item):
                # We have a site root, which works as a fallback
                for c in missing:
                    translations[c] = item
                break

            translatable = ITranslatable(item, None)
            if translatable is None:
                continue

            item_trans = item.getTranslations(review_state=False)
            for code, trans in item_trans.items():
                code = str(code)
                if code not in translations:
                    # If we don't yet have a translation for this language
                    # add it and mark it as found
                    translations[code] = trans
                    missing = missing - set((code, ))

            if len(missing) <= 0:
                # We have translations for all
                break
            if INavigationRoot.providedBy(item):
                # Don't break out of the navigation root jail, we assume
                # the INavigationRoot is usually translated into all languages
                for c in missing:
                    translations[c] = item
                break
        return translations

    def _findpath(self, path, path_info):
        # We need to find the actual translatable content object. As an
        # optimization we assume it is one of the last three path segments
        match = filter(None, path[-3:])
        current_path = filter(None, path_info.split('/'))
        append_path = []
        stop = False
        while current_path and not stop:
            check = current_path.pop()
            if check == 'VirtualHostRoot' or check.startswith('_vh_'):
                # Once we hit a VHM marker, we should stop
                break
            if check not in match:
                append_path.insert(0, check)
            else:
                stop = True
        if append_path:
            append_path.insert(0, '')
        return append_path

    def _formvariables(self, form):
        formvariables = {}
        for k, v in form.items():
            if isinstance(v, unicode):
                formvariables[k] = v.encode('utf-8')
            else:
                formvariables[k] = v
        return formvariables

    def languages(self):
        context = aq_inner(self.context)
        results = LanguageSelector.languages(self)
        supported_langs = [v['code'] for v in results]
        missing = set([str(c) for c in supported_langs])
        translations = self._translations(missing)

        # We want to preserve the current template / view as used for the
        # current object and also use it for the other languages
        append_path = self._findpath(context.getPhysicalPath(),
                                     self.request.get('PATH_INFO', ''))
        formvariables = self._formvariables(self.request.form)

        for data in results:
            code = str(data['code'])
            data['translated'] = code in translations

            try:
                appendtourl = '/'.join(append_path) + '?' + \
                    make_query(formvariables, dict(set_language=code))
            except UnicodeError:
                appendtourl = '/'.join(append_path) + '?set_language=' + code

            if data['translated']:
                trans = translations[code]
                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.canonical_object_url() + appendtourl
            else:
                state = getMultiAdapter((context, self.request),
                        name='plone_context_state')
                try:
                    data['url'] = state.canonical_object_url() + appendtourl
                except AttributeError:
                    data['url'] = context.absolute_url() + appendtourl

        return results
