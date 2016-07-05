from logging import getLogger

from plone.indexer.interfaces import IIndexableObjectWrapper
from zope.interface import implementer

from AccessControl import ClassSecurityInfo
from AccessControl import Permissions
from App.class_init import InitializeClass
from BTrees.IOBTree import IOBTree
from BTrees.IIBTree import IISet
from BTrees.IIBTree import union as ii_union
from BTrees.OOBTree import OOBTree, OOSet, OOTreeSet
from BTrees.OOBTree import union as oo_union
from BTrees.Length import Length
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluginIndexes.common.util import parseIndexRequest
from Products.PluginIndexes.interfaces import IUniqueValueIndex
from Products.PluginIndexes.interfaces import ISortIndex

from interfaces import ILanguageIndex
from Products.LinguaPlone.interfaces import ITranslatable
from utils import splitLanguage

GLOBALS = globals()
LOG = getLogger('LinguaPlone.LanguageIndex')
_marker = object()


class IndexEntry:
    """LanguageIndex entry

    Stores catalog id, main and sublanguage components, and canonical content
    id. When used as mapping keys, these indexes are deemed the same object
    when their canonical id is identical, avoiding returning multiple
    translations of the same content.
    """

    def __init__(self, docid, main, sub, cid):
        self.docid = docid
        self.main = main
        self.sub = sub
        self.cid = cid

    def __str__(self):
        # form a 'main-sub' language tag, or main if sub is None
        return '-'.join(filter(None, (self.main, self.sub)))

    def __repr__(self):
        return '<LanguageIndex.IndexEntry id %s language %s, cid %s>' % (
            self.docid, str(self), self.cid)

    # Mapping key functions, cid is the actual key
    def __hash__(self):
        return hash(self.cid)

    def __cmp__(self, other):
        return cmp(self.cid, other.cid)


@implementer(ILanguageIndex, IUniqueValueIndex, ISortIndex)
class LanguageIndex(SimpleItem, PropertyManager):

    _properties = (
        dict(id='fallback', type='boolean', mode='w'),
    )

    meta_type = 'LanguageIndex'

    manage_options = PropertyManager.manage_options + (
        dict(label='Histogram', action='manage_histogram'), )

    security = ClassSecurityInfo()

    security.declareProtected(Permissions.manage_zcatalog_indexes,
                              'manage_histogram')
    manage_histogram = PageTemplateFile('www/indexHistogram.pt', GLOBALS,
                                        __name__='manage_histogram')

    query_options = ('query', 'fallback')
    fallback = True

    def __init__(self, id, fallback=True, extra=None, caller=None):
        self.id = id
        # 'extra' is used by the twisted ZCatalog addIndex machinery
        self.fallback = extra and extra.fallback or fallback
        self.clear()

    # IPluggableIndex implementation

    security.declarePrivate('getEntryForObject')
    def getEntryForObject(self, documentId, default=None):
        """Return the documentId entry"""
        return self._unindex.get(documentId, default)

    security.declarePrivate('getIndexSourceNames')
    def getIndexSourceNames(self):
        """The attributes we index"""
        # Not configurable; only GS uses this
        return None

    security.declarePrivate('index_object')
    def index_object(self, documentId, obj, treshold=None):
        """Index the object"""
        if not ITranslatable.providedBy(obj):
            if IIndexableObjectWrapper.providedBy(obj):
                # wrapped object in `plone.indexer`
                wrapped = getattr(obj, '_IndexableObjectWrapper__object', None)
                # XXX: the rest can probably go now...
                # Wrapper doesn't proxy __implements__
                if wrapped is None:
                    wrapped = getattr(obj, '_IndexableObjectWrapper__ob', None)
                # Older CMFPlone
                if wrapped is None:
                    wrapped = getattr(obj, '_obj', None)
                if wrapped is None:
                    return 0
                obj = wrapped

        try:
            language = obj.Language
            if callable(language):
                language = language()
        except AttributeError:
            return 0

        if ITranslatable.providedBy(obj):
            canonical = obj.getCanonical()
            # Gracefully deal with broken references
            if canonical is None:
                return 0
            cid = canonical.UID()
        else:
            # Also index non-translatable content, otherwise
            # LinguaPlone only shows translatable content.
            # This assumes a catalog documentId will never
            # be equal to a UID.
            cid = documentId

        if documentId not in self._unindex:
            self._length.change(1)
        else:
            self._remove(self._unindex[documentId])

        main, sub = splitLanguage(language)
        entry = IndexEntry(documentId, main, sub, cid)
        self._insert(entry)
        self._unindex[documentId] = entry
        self._sortindex[documentId] = str(entry)

        return 1

    security.declarePrivate('unindex_object')
    def unindex_object(self, documentId):
        """Remove indexed information"""
        entry = self._unindex.get(documentId, None)

        if entry is None:
            LOG.debug('Attempt to unindex document with id %s failed'
                      % documentId)
            return

        self._remove(entry)

        self._length.change(-1)
        del self._unindex[documentId]
        del self._sortindex[documentId]

    security.declarePrivate('_apply_index')
    def _apply_index(self, request, cid=''):
        """Apply the index to the search parameters given in request"""

        record = parseIndexRequest(request, self.id, self.query_options)
        if record.keys is None:
            return None

        result = None
        fallback = self.fallback
        if hasattr(record, 'fallback'):
            fallback = bool(record.fallback)

        for language in record.keys:
            rows = self._search(language, fallback)
            result = ii_union(result, rows)

        return (result or IISet()), ('Language', )

    security.declareProtected(
        Permissions.manage_zcatalog_indexes, 'numObjects')
    def numObjects(self):
        """Return the number of indexed objects"""
        return len(self)
    indexSize = numObjects

    security.declareProtected(Permissions.manage_zcatalog_indexes, 'clear')
    def clear(self):
        """Clear the index"""
        self._index = OOBTree()
        self._unindex = IOBTree()
        self._sortindex = IOBTree()
        self._length = Length()

    # IUniqueValueIndex implementation

    security.declarePrivate('hasUniqueValuesFor')
    def hasUniqueValuesFor(self, name):
        """Return true if the index can return the unique values for name"""
        # Never actually used anywhere in the Zope and Plone codebases..
        return name == self.id

    security.declareProtected(Permissions.manage_zcatalog_indexes,
                              'uniqueValues')
    def uniqueValues(self, name=None, withLengths=False):
        """Return the unique values for name.

        If 'withLengths' is true, returns a sequence of tuples of
        (value, length).

        """
        if name is not None and name != self.id:
            # Never actually used anywhere in the Zope and Plone codebases..
            return ()

        def makeTag(main, sub):
            return '-'.join(filter(None, (main, sub)))

        if withLengths:
            return tuple((makeTag(m, s), len(entries))
                         for (m, subs) in self._index.items()
                         for (s, entries) in subs.items())
        else:
            return tuple(makeTag(m, s)
                         for (m, subs) in self._index.items()
                         for s in subs.keys())

    # ISortIndex implementation

    security.declarePrivate('keyForDocument')
    def keyForDocument(self, documentId):
        """Deprecated"""
        return self._sortindex[documentId]

    security.declarePrivate('documentToKeyMap')
    def documentToKeyMap(self):
        """Map id to language tag"""
        return self._sortindex

    # Internal operations

    security.declarePrivate('__len__')
    def __len__(self):
        return self._length()

    security.declarePrivate('_insert')
    def _insert(self, entry):
        if entry.main not in self._index:
            self._index[entry.main] = OOBTree()
        if entry.sub not in self._index[entry.main]:
            self._index[entry.main][entry.sub] = OOTreeSet()

        self._index[entry.main][entry.sub].insert(entry)

    security.declarePrivate('_remove')
    def _remove(self, entry):
        main = self._index.get(entry.main, _marker)
        if main is _marker:
            return

        # XXX I get many spurious errors on trying to remove the entry here,
        # which is strange. If the entry exists in _unindex, it should
        # be in _index[entry.main][entry.sub] as well.
        # I've put a test around it now, but this might hide a deeper problem.
        # //regebro
        if entry in self._index[entry.main][entry.sub]:
            self._index[entry.main][entry.sub].remove(entry)
        else:
            LOG.warning("entry %s existed in _unindex "
                        "but not in _index." % str(entry))

        if not self._index[entry.main][entry.sub]:
            del self._index[entry.main][entry.sub]
        if not self._index[entry.main]:
            del self._index[entry.main]

    security.declarePrivate('_search')
    def _search(self, language, fallback=True):
        main, sub = splitLanguage(language)

        if main not in self._index:
            return None

        if fallback:
            # Search in sorted order, specific sub tag first, None second
            subs = list(self._index[main].keys())
            subs.sort()
            if sub in subs:
                subs.remove(sub)
                subs.insert(0, sub)
        else:
            subs = [sub]

        result = OOSet()

        for sublanguage in subs:
            result = oo_union(result, self._index[main][sublanguage])

        return IISet(entry.docid for entry in result)

InitializeClass(LanguageIndex)


manage_addLanguageIndexForm = PageTemplateFile('www/addLanguageIndex.pt',
                                               GLOBALS)


def manage_addLanguageIndex(self, id, extra=None, REQUEST=None, RESPONSE=None,
                            URL3=None):
    """Add a LanguageIndex to the catalog (with the strange indirection)"""
    return self.manage_addIndex(id, 'LanguageIndex', extra, REQUEST, RESPONSE,
                                URL3)
