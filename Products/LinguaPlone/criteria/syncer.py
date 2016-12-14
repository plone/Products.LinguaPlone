from zope.component import adapts
from zope.component import queryAdapter
from zope.interface import implementer

from Acquisition import aq_parent
from Products.ATContentTypes.interfaces import IATTopicCriterion
from Products.ATContentTypes.interfaces import IATTopic
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.criteria.interfaces import ICollectionSyncer
from Products.LinguaPlone.criteria.interfaces import ICriterionSyncer
from Products.LinguaPlone.interfaces import ITranslatable
from Products.LinguaPlone.utils import translated_references


def sync_collections(context):
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(context.getPhysicalPath())
    for brain in catalog(path=path, portal_type='Topic', Language='all'):
        try:
            obj = brain.getObject()
        except AttributeError: # pragma: no cover
            # catalogs are broken too often
            continue

        if obj.isCanonical():
            syncer = queryAdapter(obj, ICollectionSyncer)
            if syncer is not None:
                syncer.sync()


@implementer(ICollectionSyncer)
class CollectionSyncer(object):

    adapts(IATTopic)

    def __init__(self, context):
        self.context = context

    def sync(self):
        collection = self.context
        translations = collection.getTranslations(
            include_canonical=False, review_state=False)
        source_criteria = collection.listCriteria()
        source_criteria_ids = [s.getId() for s in source_criteria]
        for trans in translations.values():
            target_criteria = trans.listCriteria()
            target_criteria_ids = [t.getId() for t in target_criteria]
            additional = set(source_criteria_ids) - set(target_criteria_ids)
            if len(additional) > 0:
                # TODO This relies on the criterias to be in the
                # addable types list for the Topic type. We should
                # try to circumvent that check
                # We might instead just add new "empty" criteria of the correct
                # type and leave it to the sync logic below to fill in the
                # right values
                # If we leave it to the sync logic, we need to handle
                # "language independent" criteria like "SimpleString". They
                # should copy the criteria and inital value, but not do
                # automatic syncing afterwards
                info = collection.manage_copyObjects(list(additional))
                trans.manage_pasteObjects(info)
            removed = set(target_criteria_ids) - set(source_criteria_ids)
            if len(removed) > 0:
                for r in removed:
                    trans.deleteCriterion(r)

            for id_ in source_criteria_ids:
                source = collection.get(id_)
                target = trans.get(id_)
                self.sync_criterion(trans, source, target)

            trans.reindexObject()

    def sync_criterion(self, translation, source, target):
        # First look up a syncer for a specific field
        syncer = queryAdapter(source, ICriterionSyncer, name=source.Field())
        if syncer is not None:
            syncer.sync(translation, target)
        else:
            # Fall back to using a generic criterion type syncer
            syncer = queryAdapter(source, ICriterionSyncer)
            if syncer is not None:
                syncer.sync(translation, target)


@implementer(ICriterionSyncer)
class CriterionSyncer(object):

    adapts(IATTopicCriterion)

    def __init__(self, context):
        self.context = context

    def sync(self, collection, criterion):
        raise NotImplemented # pragma: no cover


class AddOnlyCriterionSyncer(CriterionSyncer):

    def sync(self, collection, criterion):
        # In general we don't want to sync the value for this criteria, but
        # we'd still want to copy it initially as a new default. This is for
        # example used for string criteria with a value like "fish".
        pass


class NoValueCriterionSyncer(CriterionSyncer):

    def sync(self, collection, criterion):
        # This criterion has no value, but always looks it up dynamically
        pass


class SchemaBasedCriterionSyncer(CriterionSyncer):

    def sync(self, collection, criterion):
        source = self.context
        schema = source.Schema()
        target_schema = criterion.Schema()
        for f in schema.fields():
            name = f.getName()
            if name in ('id', 'field'):
                continue

            source_value = f.get(source)
            target_field = target_schema.getField(name)
            value = target_field.get(criterion)

            if value != source_value:
                target_field.set(criterion, source_value)


class ReferenceCriterionSyncer(CriterionSyncer):

    def sync(self, collection, criterion):
        # If we copy reference criteria, we need to
        # adjust their reference to the correct UID in
        # the new language
        source_value = self.context.Value()
        language = collection.Language()
        value = criterion.Value()
        if source_value:
            new_value = translated_references(
                collection, language, list(source_value))
            if list(value) != new_value:
                criterion.setValue(new_value)


class PathCriterionSyncer(ReferenceCriterionSyncer):

    def sync(self, collection, criterion):
        # Take care of the value field consisting of UID's
        ReferenceCriterionSyncer.sync(self, collection, criterion)
        # Copy the additional recurse field
        source_value = self.context.Recurse()
        value = criterion.Recurse()
        if value != source_value:
            criterion.setRecurse(source_value)


class RelativePathCriterionSyncer(CriterionSyncer):

    def sync(self, collection, criterion):
        # Take care of the value field
        source_value = self.context.getRelativePath()
        value = criterion.getRelativePath()
        # This is tricky. The relative path can contain the ids of
        # folders, which we'd need to translate
        norm_source_value = source_value.replace('\\', '/')
        norm_source_value = source_value.replace('.', '').replace('/', '')
        if len(norm_source_value) > 0:
            # We have ids in the value
            self._sync_withids(collection, criterion, value, source_value)
        elif source_value != value:
            criterion.setRelativePath(source_value)

        # Copy the additional recurse field
        source_value = self.context.Recurse()
        value = criterion.Recurse()
        if value != source_value:
            criterion.setRecurse(source_value)

    def _sync_withids(self, collection, criterion, value, source_value):
        source_coll = aq_parent(self.context)
        # Filter out simple dots as in '.././foo' and normalize backslashes
        norm_value = source_value.replace('\\', '/').split('/')
        norm_value = '/'.join([n for n in norm_value if n != '.'])
        try:
            source_obj = source_coll.unrestrictedTraverse(norm_value)
        except (AttributeError, KeyError):
            # The source object couldn't be found, keep the value
            criterion.setRelativePath(source_value)
            return

        language = collection.Language()
        obj = None
        if ITranslatable.providedBy(source_obj):
            obj = source_obj.getTranslation(language)
        if obj is not None:
            obj_path = obj.getPhysicalPath()
            source_path = source_obj.getPhysicalPath()
            target_value = source_value.split('/')
            # What follows assumes that the distance between the source
            # collection and source object is the same as the one in the
            # translated language
            ppath = zip(source_path, obj_path)
            len_ppath = len(ppath)
            for pos, (s, t) in enumerate(ppath):
                reverse_pos = pos - len_ppath
                if s == t:
                    # skip the common root elements
                    continue
                elif target_value[reverse_pos] == s:
                    # replace the id with the translated id
                    target_value[reverse_pos] = t
                else:
                    # Mismatching ids covered by a '..'
                    pass
            target_value = '/'.join(target_value)
            criterion.setRelativePath(target_value)
            return

        # If we cannot figure things out, we set the source
        criterion.setRelativePath(source_value)
