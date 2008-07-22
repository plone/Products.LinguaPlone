from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from plone.app.i18n.locales.browser.selector import LanguageSelector


class TranslatableLanguageSelector(LanguageSelector):
    """Language selector for translatable content.
    """

    render = ZopeTwoPageTemplateFile('selector.pt')

    def languages(self):
        results = LanguageSelector.languages(self)
        translations = self.context.getTranslations()

        for data in results:
            data['translated'] = data['code'] in translations
            if data['translated']:
                trans = translations[data['code']][0]
                state = queryMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']
            else:
                state = queryMultiAdapter((self.context, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']

        return results


