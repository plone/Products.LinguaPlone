from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.LinguaPlone.interfaces import ITranslatable
from plone.app.i18n.locales.browser.selector import LanguageSelector


class TranslatableLanguageSelector(LanguageSelector):
    """Language selector for translatable content.
    """

    render = ZopeTwoPageTemplateFile('selector.pt')

    def languages(self):
        results = LanguageSelector.languages(self)
        translatable = ITranslatable(self.context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

        for data in results:
            data['translated'] = data['code'] in translations
            if data['translated']:
                trans = translations[data['code']][0]
                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']
            else:
                state = getMultiAdapter((self.context, self.request),
                        name='plone_context_state')
                try:
                    data['url'] = state.view_url() + '?set_language=' + data['code']
                except AttributeError:
                    data['url'] = self.context.absolute_url() + '?set_language=' + data['code']

        return results


