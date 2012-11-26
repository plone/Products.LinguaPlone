from DateTime import DateTime
from Missing import MV
from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.criteria.syncer import sync_collections

CRITERIA_TYPES = (
    'ATBooleanCriterion',
    'ATCurrentAuthorCriterion',
    'ATDateCriteria',
    'ATDateRangeCriterion',
    'ATListCriterion',
    'ATPathCriterion',
    'ATPortalTypeCriterion',
    'ATReferenceCriterion',
    'ATRelativePathCriterion',
    'ATSelectionCriterion',
    'ATSimpleIntCriterion',
    'ATSimpleStringCriterion',
    'ATSortCriterion',
)


class CopyCriteriaTestCase(LinguaPloneTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addLanguage('no')
        self.addLanguage('sv')
        self.setLanguage('en')

        # TODO We currently need to have criteria being addable to collections
        ttool = getToolByName(self.portal, 'portal_types')
        ttool['Topic'].allowed_content_types = tuple(CRITERIA_TYPES)
        ttool['Topic'].global_allow = True

        self.folder.invokeFactory('Folder', 'test-english')
        self.en = en = self.folder.get('test-english')
        en.addTranslation('no')
        self.no = en.getTranslation('no')
        en.invokeFactory('Document', 'doc1')
        en.doc1.addTranslation('no')
        en.invokeFactory('Document', 'doc2')
        en.doc2.addTranslation('no')
        en.invokeFactory('Topic', 'coll')
        self.encoll = encoll = en.coll
        encoll.addTranslation('no')
        self.nocoll = encoll.getTranslation('no')


class TestBasics(CopyCriteriaTestCase):

    def testEmptyCollection(self):
        self.assert_('coll' in self.en)
        self.assert_(self.nocoll.getId() in self.no)
        sync_collections(self.encoll)
        self.assert_(self.nocoll.getId() in self.no)

    def testAddCriteria(self):
        crit = self.encoll.addCriterion('portal_type', 'ATPortalTypeCriterion')
        crit.setValue(['Document'])
        self.assertEquals(len(self.encoll.listCriteria()), 1)

        # Check the criteria have been copied over
        sync_collections(self.encoll)
        self.assertEquals(len(self.nocoll.listCriteria()), 1)

        # Add a new criteria
        crit = self.encoll.addCriterion('boolean', 'ATBooleanCriterion')
        crit.setBool(True)
        self.assertEquals(len(self.encoll.listCriteria()), 2)

        sync_collections(self.encoll)
        self.assertEquals(len(self.nocoll.listCriteria()), 2)

    def testRemoveCriteria(self):
        crit = self.encoll.addCriterion('portal_type', 'ATPortalTypeCriterion')
        crit.setValue(['Document'])
        crit = self.encoll.addCriterion('boolean', 'ATBooleanCriterion')
        crit.setBool(True)
        self.assertEquals(len(self.encoll.listCriteria()), 2)
        sync_collections(self.encoll)
        self.assertEquals(len(self.nocoll.listCriteria()), 2)

        # Remove a criteria
        one_id = self.encoll.listCriteria()[0].getId()
        self.encoll.deleteCriterion(one_id)
        self.assertEquals(len(self.encoll.listCriteria()), 1)
        sync_collections(self.encoll)
        self.assertEquals(len(self.nocoll.listCriteria()), 1)


class TestCopyCriteria(CopyCriteriaTestCase):

    def testFieldSpecificSyncer(self):
        crit = self.encoll.addCriterion(
            'review_state', 'ATSimpleStringCriterion')
        crit.setValue('published')
        query = self.encoll.buildQuery()
        self.assertEquals(query, {'review_state': 'published'})

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query, {'review_state': 'published'})

        # See if changes to the criterion are copied
        crit.setValue('private')
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query, {'review_state': 'private'})

    def testBooleanCriterion(self):
        crit = self.encoll.addCriterion('boolean', 'ATBooleanCriterion')
        crit.setBool(True)
        query = self.encoll.buildQuery()
        self.assertEquals(query, {'boolean': [1, True, '1', 'True']})

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query, {'boolean': [1, True, '1', 'True']})

        # See if changes to the criterion are copied
        crit.setBool(False)
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query,
            {'boolean': [0, '', False, '0', 'False', None, (), [], {}, MV]})

    def testCurrentAuthorCriterion(self):
        self.encoll.addCriterion('author', 'ATCurrentAuthorCriterion')
        query = self.encoll.buildQuery()
        self.assertEquals(query, {'author': 'portal_owner'})

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query, {'author': 'portal_owner'})

    def testDateCriterion(self):
        crit = self.encoll.addCriterion('modified', 'ATFriendlyDateCriteria')
        crit.setValue(31)
        crit.setDateRange('+')
        crit.setOperation('less')

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocrit = self.nocoll.get(crit.getId())
        self.assertEquals(nocrit.Value(), crit.Value())
        self.assertEquals(nocrit.getDateRange(), crit.getDateRange())
        self.assertEquals(nocrit.getOperation(), crit.getOperation())

        # See if changes to the criterion are copied
        crit.setValue(14)
        crit.setOperation('more')
        sync_collections(self.encoll)
        self.assertEquals(nocrit.Value(), crit.Value())
        self.assertEquals(nocrit.getDateRange(), crit.getDateRange())
        self.assertEquals(nocrit.getOperation(), crit.getOperation())

    def testDateRangeCriterion(self):
        crit = self.encoll.addCriterion('modified', 'ATDateRangeCriterion')
        start = DateTime('2010-02-14')
        end = DateTime('2010-02-25')
        crit.setStart(start)
        crit.setEnd(end)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocrit = self.nocoll.get(crit.getId())
        self.assertEquals(crit.getStart(), start)
        self.assertEquals(crit.getEnd(), end)

        # See if changes to the criterion are copied
        crit.setStart(start + 1)
        crit.setEnd(end + 1)
        sync_collections(self.encoll)
        self.assertEquals(nocrit.getStart(), start + 1)
        self.assertEquals(nocrit.getEnd(), end + 1)

    def testListCriterion(self):
        crit = self.encoll.addCriterion('subject', 'ATListCriterion')
        crit.setValue(('tag1', 'tag2'))
        crit.setOperator('and')

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocrit = self.nocoll.get(crit.getId())
        self.assertEquals(nocrit.Value(), ('tag1', 'tag2'))
        self.assertEquals(nocrit.getOperator(), 'and')

        # See if changes to the criterion are copied
        crit.setValue(('tag3', 'tag2'))
        crit.setOperator('or')
        sync_collections(self.encoll)
        self.assertEquals(nocrit.Value(), ('tag3', 'tag2'))
        self.assertEquals(nocrit.getOperator(), 'or')

    def testPathCriterion(self):
        crit = self.encoll.addCriterion('path', 'ATPathCriterion')
        endoc = self.en.doc1
        enpath = '/'.join(endoc.getPhysicalPath())
        crit.setValue((endoc.UID(), ))
        crit.setRecurse(True)
        query = self.encoll.buildQuery()
        self.assertEquals(query['path']['query'], [enpath])
        self.assertEquals(query['path']['depth'], -1)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nodoc = endoc.getTranslation('no')
        nopath = '/'.join(nodoc.getPhysicalPath())
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], [nopath])
        self.assertEquals(query['path']['depth'], -1)

        # See if changes to the criterion are copied
        endoc2 = self.en.doc2
        crit.setValue((endoc.UID(), endoc2.UID()))
        crit.setRecurse(False)

        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        nodoc2 = endoc2.getTranslation('no')
        nopath2 = '/'.join(nodoc2.getPhysicalPath())
        self.assertEquals(sorted(query['path']['query']),
            sorted([nopath, nopath2]))
        self.assertEquals(query['path']['depth'], 1)

    def testPortalTypeCriterion(self):
        crit = self.encoll.addCriterion(
            'portal_type', 'ATPortalTypeCriterion')
        crit.setValue(['Document', 'News Item'])
        query = self.encoll.buildQuery()
        self.assertEquals(query, {'portal_type': ('Document', 'News Item')})

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query, {'portal_type': ('Document', 'News Item')})

        # See if changes to the criterion are copied
        crit.setValue(['Document', 'Image'])
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query, {'portal_type': ('Document', 'Image')})

    def testReferenceCriterion(self):
        crit = self.encoll.addCriterion(
            'getRawRelatedItems', 'ATReferenceCriterion')
        endoc = self.en.doc1
        crit.setValue(endoc.UID())
        query = self.encoll.buildQuery()['getRawRelatedItems']['query']
        self.assertEquals(query, (endoc.UID(), ))

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()['getRawRelatedItems']['query']
        nodoc = endoc.getTranslation('no')
        self.assertEquals(query, (nodoc.UID(), ))

        # See if changes to the criterion are copied
        endoc2 = self.en.doc2
        crit.setValue(endoc2.UID())
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()['getRawRelatedItems']['query']
        nodoc2 = endoc2.getTranslation('no')
        self.assertEquals(query, (nodoc2.UID(), ))

    def testSelectionCriterion(self):
        crit = self.encoll.addCriterion('select', 'ATSelectionCriterion')
        crit.setValue(('tag1', 'tag2'))
        crit.setOperator('and')

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocrit = self.nocoll.get(crit.getId())
        self.assertEquals(nocrit.Value(), ('tag1', 'tag2'))
        self.assertEquals(nocrit.getOperator(), 'and')

        # See if changes to the criterion are copied
        crit.setValue(('tag3', 'tag2'))
        crit.setOperator('or')
        sync_collections(self.encoll)
        self.assertEquals(nocrit.Value(), ('tag3', 'tag2'))
        self.assertEquals(nocrit.getOperator(), 'or')

    def testSimpleIntCriterion(self):
        crit = self.encoll.addCriterion('integer', 'ATSimpleIntCriterion')
        crit.setValue(1)
        crit.setValue2(2)
        crit.setDirection('min:max')

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocrit = self.nocoll.get(crit.getId())
        self.assertEquals(nocrit.Value(), 1)
        self.assertEquals(nocrit.Value2(), 2)
        self.assertEquals(nocrit.getDirection(), 'min:max')

        # See if changes to the criterion are copied
        crit.setValue(7)
        crit.setValue2(5)
        crit.setDirection('max')
        sync_collections(self.encoll)
        self.assertEquals(nocrit.Value(), 7)
        self.assertEquals(nocrit.Value2(), 5)
        self.assertEquals(nocrit.getDirection(), 'max')

    def testSimpleStringCriterion(self):
        crit = self.encoll.addCriterion('string', 'ATSimpleStringCriterion')
        crit.setValue('foo')

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocrit = self.nocoll.get(crit.getId())
        self.assertEquals(nocrit.Value(), 'foo')

        # Change the value in the translation
        nocrit.setValue('bar')

        # Make sure the changes aren't clobbered
        crit.setValue('baz')
        sync_collections(self.encoll)
        self.assertEquals(nocrit.Value(), 'bar')

    def testSortCriterion(self):
        crit = self.encoll.addCriterion('sort', 'ATSortCriterion')
        crit.setReversed(True)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocrit = self.nocoll.get(crit.getId())
        self.assertEquals(nocrit.getReversed(), True)

        # See if changes to the criterion are copied
        crit.setReversed(False)
        sync_collections(self.encoll)
        self.assertEquals(nocrit.getReversed(), False)


class TestCopyRelativePathCriteria(CopyCriteriaTestCase):

    def testRecurse(self):
        crit = self.encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('.')
        crit.setRecurse(True)

        encollpath = '/'.join(self.encoll.getPhysicalPath())
        query = self.encoll.buildQuery()
        self.assertEquals(query['path']['query'], encollpath)
        self.assertEquals(query['path']['depth'], -1)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocollpath = '/'.join(self.nocoll.getPhysicalPath())
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], nocollpath)
        self.assertEquals(query['path']['depth'], -1)

        # See if changes to the criterion are copied
        crit.setRecurse(False)
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], nocollpath)
        self.assertEquals(query['path']['depth'], 1)

    def testCurrentFolder(self):
        crit = self.encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('.')
        encollpath = '/'.join(self.encoll.getPhysicalPath())
        query = self.encoll.buildQuery()
        self.assertEquals(query['path']['query'], encollpath)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        nocollpath = '/'.join(self.nocoll.getPhysicalPath())
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], nocollpath)

        # See if changes to the criterion are copied
        crit.setRecurse(False)
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['depth'], 1)

    def testParentFolder(self):
        crit = self.encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('..')

        enparent_path = '/'.join(self.en.getPhysicalPath())
        query = self.encoll.buildQuery()
        self.assertEquals(query['path']['query'], enparent_path)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        noparent_path = '/'.join(self.no.getPhysicalPath())
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], noparent_path)

        # See if changes to the criterion are copied
        crit.setRelativePath('../')
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], noparent_path + '/')

    def testParentParentFolder(self):
        crit = self.encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('../..')

        folder_path = '/'.join(self.folder.getPhysicalPath())
        query = self.encoll.buildQuery()
        self.assertEquals(query['path']['query'], folder_path)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], folder_path)

        # See if changes to the criterion are copied
        crit.setRelativePath('../../../..')
        sync_collections(self.encoll)
        portal_path = '/'.join(self.portal.getPhysicalPath())
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], portal_path)

    def testRootFolder(self):
        crit = self.encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('/')

        portal_path = '/'.join(self.portal.getPhysicalPath()) + '/'
        query = self.encoll.buildQuery()
        self.assertEquals(query['path']['query'], portal_path)

        # Check the criterion has been copied over
        sync_collections(self.encoll)
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], portal_path)

        # See if changes to the criterion are copied
        crit.setRelativePath('..')
        sync_collections(self.encoll)
        noparent_path = '/'.join(self.no.getPhysicalPath())
        query = self.nocoll.buildQuery()
        self.assertEquals(query['path']['query'], noparent_path)


class TestCopyRelativePathCriteriaWithIds(LinguaPloneTestCase):

    def afterSetUp(self):
        # Build the following structure:
        # /
        # \-en1
        #   \-en11
        # \-en2
        #   \-en21
        #   \-en22
        # \-no1
        #   \-no11
        # \-no2
        #   \-no21
        # \-sv1
        self.loginAsPortalOwner()
        self.addLanguage('no')
        self.addLanguage('sv')
        self.setLanguage('en')

        # TODO We currently need to have criteria being addable to collections
        ttool = getToolByName(self.portal, 'portal_types')
        ttool['Topic'].allowed_content_types = tuple(CRITERIA_TYPES)
        ttool['Topic'].global_allow = True

        self.en1 = self._create(self.folder, 'Folder', 'en1', 'no1', 'sv1')
        self.en2 = self._create(self.folder, 'Folder', 'en2', 'no2', None)
        self.en11 = self._create(self.en1, 'Folder', 'en11', 'no11', None)
        self.en21 = self._create(self.en2, 'Folder', 'en21', 'no21', None)
        self.en22 = self._create(self.en2, 'Folder', 'en22', None, None)

    def _create(self, parent, tname, name, lname1, lname2):
        # parent, type name, id of the canonical folder, id of the first
        # and second translation starting with the language code
        parent.invokeFactory(tname, name)
        folder = parent.get(name)
        if lname1 is not None:
            folder.addTranslation(lname1[:2])
        if lname2 is not None:
            folder.addTranslation(lname2[:2])
        return folder

    def testRootFolder(self):
        encoll = self._create(self.en1, 'Topic', 'encoll', 'nocoll', 'svcoll')
        crit = encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('/')

        portal_path = '/'.join(self.portal.getPhysicalPath()) + '/'
        query = encoll.buildQuery()
        self.assertEquals(query['path']['query'], portal_path)

        # Check the criterion has been copied over
        sync_collections(encoll)
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], portal_path)

        # See if changes to the criterion are copied
        crit.setRelativePath('/missing')
        sync_collections(encoll)
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], portal_path + 'missing')

        query = encoll.getTranslation('sv').buildQuery()
        self.assertEquals(query['path']['query'], portal_path + 'missing')

    def testParentFolder(self):
        encoll = self._create(self.en1, 'Topic', 'encoll', 'nocoll', 'svcoll')
        crit = encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('../encoll')

        path = '/'.join(encoll.getPhysicalPath())
        query = encoll.buildQuery()
        self.assertEquals(query['path']['query'], path)

        # Check the criterion has been copied over
        sync_collections(encoll)
        path = '/'.join(encoll.getTranslation('no').getPhysicalPath())
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], path)

        # See if changes to the criterion are copied
        crit.setRelativePath('.././encoll')
        sync_collections(encoll)
        path = '/'.join(encoll.getTranslation('no').getPhysicalPath())
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], path)

        path = '/'.join(encoll.getTranslation('sv').getPhysicalPath())
        query = encoll.getTranslation('sv').buildQuery()
        self.assertEquals(query['path']['query'], path)

    def testParentParentFolder(self):
        encoll = self._create(self.en1, 'Topic', 'encoll', 'nocoll', 'svcoll')
        crit = encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('../../en2')

        path = '/'.join(self.en2.getPhysicalPath())
        query = encoll.buildQuery()
        self.assertEquals(query['path']['query'], path)

        # Check the criterion has been copied over
        sync_collections(encoll)
        path = '/'.join(self.en2.getTranslation('no').getPhysicalPath())
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], path)

        # See if changes to the criterion are copied
        crit.setRelativePath('../../en1')
        sync_collections(encoll)
        path = '/'.join(self.en1.getTranslation('no').getPhysicalPath())
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], path)

        path = '/'.join(self.en1.getTranslation('sv').getPhysicalPath())
        query = encoll.getTranslation('sv').buildQuery()
        self.assertEquals(query['path']['query'], path)

    def testParentParentMissingFolder(self):
        encoll = self._create(self.en21, 'Topic', 'encoll', 'nocoll', 'svcoll')
        crit = encoll.addCriterion('path', 'ATRelativePathCriterion')
        crit.setRelativePath('../../en21')

        path = '/'.join(self.en21.getPhysicalPath())
        query = encoll.buildQuery()
        self.assertEquals(query['path']['query'], path)

        # Check the criterion has been copied over
        sync_collections(encoll)
        path = '/'.join(self.en21.getTranslation('no').getPhysicalPath())
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], path)

        # See if changes to the criterion are copied
        crit.setRelativePath('../../en22')
        sync_collections(encoll)
        # There's no full Norwegian translation chain
        path = '/'.join(self.en2.getTranslation('no').getPhysicalPath())
        query = encoll.getTranslation('no').buildQuery()
        self.assertEquals(query['path']['query'], path + '/en22')
        nocoll_criteria = encoll.getTranslation('no').listCriteria()
        self.assertEquals(nocoll_criteria[0].getRelativePath(), '../../en22')

        query = encoll.getTranslation('sv').buildQuery()
        # There's no Swedish translation at all
        path = '/'.join(self.en22.getPhysicalPath())
        self.assertEquals(query['path']['query'], path)
        svcoll_criteria = encoll.getTranslation('sv').listCriteria()
        self.assertEquals(svcoll_criteria[0].getRelativePath(), '../../en22')
