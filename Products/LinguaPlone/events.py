from zope.interface import implements
from zope.interface import Attribute
from zope.component.interfaces import IObjectEvent


class IObjectWillBeTranslatedEvent(IObjectEvent):
    """Sent before an object is translated."""

    object = Attribute("The object to be translated.")
    language = Attribute("Target language.")


class IObjectTranslatedEvent(IObjectEvent):
    """Sent after an object was translated."""

    object = Attribute("The object to be translated.")
    target = Attribute("The translation target object.")
    language = Attribute("Target language.")


class ObjectWillBeTranslatedEvent(object):
    """Sent before an object is translated."""
    implements(IObjectWillBeTranslatedEvent)

    def __init__(self, context, language):
        self.object = context
        self.language = language


class ObjectTranslatedEvent(object):
    """Sent after an object was translated."""
    implements(IObjectTranslatedEvent)

    def __init__(self, context, target, language):
        self.object = context
        self.target = target
        self.language = language
