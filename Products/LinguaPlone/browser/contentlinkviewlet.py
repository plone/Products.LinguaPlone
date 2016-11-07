from Acquisition import aq_inner
from AccessControl.SecurityManagement import getSecurityManager

from plone.app.layout.viewlets import ViewletBase

class MultilingualContentViewlet(ViewletBase):

    def update(self):
        # We have to check the view permission on the translated object, because
        # getTranslations returns all objects, no matter the workflow state
        context = aq_inner(self.context)
        _checkPermission = getSecurityManager().checkPermission
        self.translations = []
        for lang, content in context.getTranslations(review_state=False).items():
            if _checkPermission('View', content):
                self.translations.append(content)
