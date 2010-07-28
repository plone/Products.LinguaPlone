# BBB Zope 2.12
try:
    from zope.browsermenu.interfaces import IBrowserMenu
    from zope.browsermenu.interfaces import IBrowserSubMenuItem # pragma: no cover
except ImportError: # pragma: no cover
    from zope.app.publisher.interfaces.browser import IBrowserMenu
    from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem


class ITranslateSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the translate menu.
    """


class ITranslateMenu(IBrowserMenu):
    """The translate menu.
    """
