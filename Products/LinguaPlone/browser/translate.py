from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from Products.LinguaPlone import LinguaPloneMessageFactory as _
from Products.CMFCore.utils import getToolByName


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

