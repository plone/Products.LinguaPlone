from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.defaultpage import DefaultPage as BaseDefaultPage

from Products.LinguaPlone.interfaces import ITranslatable


class DefaultPage(BaseDefaultPage):

    def getDefaultPage(self):
        """Get the translation of the folder default page in current language
        if folder is neutral
        """
        default_page = super(DefaultPage, self).getDefaultPage()
        if not default_page:
            return default_page

        if self.context.Language():
            return default_page

        page = self.context[default_page]
        languageTool = getToolByName(self.context, 'portal_languages')
        current = languageTool.getPreferredLanguage()
        if page.hasTranslation(current):
            return page.getTranslation(current).getId()
        else:
            return default_page

    def isDefaultPage(self, obj):
        default_page = super(DefaultPage, self).getDefaultPage()
        if obj.getId() == default_page:
            return True

        if ITranslatable.providedBy(obj):
            for translation in obj.getTranslations(review_state=False).values():
                if translation.getId() == default_page:
                    return True

        return False
