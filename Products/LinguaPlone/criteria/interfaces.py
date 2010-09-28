from zope.interface import Interface


class ICollectionSyncer(Interface):

    def __init__(context):
        """The source collection object."""

    def sync():
        """Syncronizes the source collection to all its translations."""


class ICriterionSyncer(Interface):

    def __init__(context):
        """The context is the source criterion object."""

    def sync(collection, criterion):
        """Syncronizes the source criterion to the target collection.
        collection is the target collection and criterion the target
        criterion object.
        """
