from plone.app.i18n.locales.browser.selector import LanguageSelector
from zope.component import getMultiAdapter

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from Products.LinguaPlone.interfaces import ITranslatable
from ZTUtils import make_query


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
        translatable = ITranslatable(context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

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
            if check not in match:
                append_path.insert(0,check)
            else:
                stop = True
        if append_path:
            append_path.insert(0, '')

        formvariables = {}
        for k,v in self.request.form.items():
            if k == '-C':
                # no idea where the -C is put into the form variables, but it
                # appears to be always there without any actual meaning
                continue
            if isinstance(v, unicode):
                formvariables[k] = v.encode('utf-8')
            else:
                formvariables[k] = v
        for data in results:
            data['translated'] = data['code'] in translations

            try:
                appendtourl = '/'.join(append_path) + \
                          '?' + make_query(formvariables, dict(set_language=data['code']))
            except UnicodeError:
                appendtourl = '/'.join(append_path) + '?set_language=' + data['code']

            if data['translated']:
                trans = translations[data['code']][0]
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
