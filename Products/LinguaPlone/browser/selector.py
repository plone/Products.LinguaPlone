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

    def languages(self):
        context = aq_inner(self.context)
        results = LanguageSelector.languages(self)
        supported_langs = [v['code'] for v in results]
        missing = set([str(c) for c in supported_langs])

        # The next part is to figure out the "closest" translation in the
        # parent chain of the context. We stop at both an INavigationRoot or
        # a ISiteRoot to look for translations.
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
            for code,trans in item_trans.items():
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

        # We want to preserve the current template / view as used for the
        # current object and also use it for the other languages

        # We need to find the actual translatable content object. As an
        # optimization we assume it is one of the last two path segments
        match = filter(None,context.getPhysicalPath()[-2:])
        current_path = filter(None, self.request.get('PATH_INFO', '').split('/'))
        append_path = []
        stop = False
        while current_path and not stop:
            check = current_path.pop()
            if check == 'VirtualHostRoot' or check.startswith('_vh_'):
                # Just ignore the VirtualHostRoot path info. This looks
                # somewhat odd, but I couldn't figure out a way to use the
                # actual request API to give us what we need
                continue
            if check not in match:
                append_path.insert(0,check)
            else:
                stop = True
        if append_path:
            append_path.insert(0, '')

        formvariables = {}
        for k,v in self.request.form.items():
            if k == '-C':
                # In Zope < 2.12.5 a -C was added whenever there was no
                # query string.
                continue # pragma: no cover
            if isinstance(v, unicode):
                formvariables[k] = v.encode('utf-8')
            else:
                formvariables[k] = v
        for data in results:
            code = str(data['code'])
            data['translated'] = code in translations

            try:
                appendtourl = '/'.join(append_path) + \
                          '?' + make_query(formvariables, dict(set_language=code))
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
