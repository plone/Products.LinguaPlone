from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem


class ITranslateSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the translate menu.
    """


class ITranslateMenu(IBrowserMenu):
    """The translate menu.
    """
