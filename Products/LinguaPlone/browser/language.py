import operator
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.LinguaPlone.interfaces import ITranslatable
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from plone.memoize.instance import memoize


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.selector = TranslatableLanguageSelector(context, request, None, None)
        self.selector.update()
        self.languages = self.selector.languages()
        self.languages.sort(key=operator.itemgetter("native"))
        portal_state = getMultiAdapter((context, request),
                                       name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()

    def show(self):
        return self.selector.available() and len(self.languages) > 1

    def showFlags(self):
        return self.selector.showFlags()

    def update(self):
        pass

    render = ViewPageTemplateFile('language.pt')

    @memoize
    def items(self):
        if not ITranslatable.providedBy(self.context):
            def plain_context(info):
                info["has_translation"]=False
            updater=plain_context
        else:
            def translatable_context(info):
                trans=self.context.getTranslation(info["code"])
                if trans is None:
                    info["has_translation"]=False
                else:
                    info["has_translation"]=True
                    state=getMultiAdapter((trans, self.request),
                            name='plone_context_state')
                    info["url"]=state.view_url()
            updater=translatable_context

        for lang in self.languages:
            updater(lang)

        return self.languages
