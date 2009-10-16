#
# Tests the PloneTool
#

from cStringIO import StringIO
from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Acquisition import Implicit

default_user = PloneTestCase.default_user

class DummyTitle(Implicit):
    def Title(self):
        # Should just return 'portal_catalog'
        tool = getToolByName(self, 'portal_catalog')
        # Use implicit acquisition even, the horror
        tool = self.portal_catalog
        return tool.getId()
    def getId(self):
        return 'foobar'


class TestPloneTool(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.utils = self.portal.plone_utils

    def testNormalizeStringPunctuation(self):
        # Punctuation and spacing is removed and replaced by '-'
        self.assertEqual(self.utils.normalizeString("a string with spaces"),
                         'a-string-with-spaces')
        self.assertEqual(self.utils.normalizeString("p.u,n;c(t)u!a@t#i$o%n"),
                         'p-u-n-c-t-u-a-t-i-o-n')

    def testNormalizeStringLower(self):
        # Strings are lowercased
        self.assertEqual(self.utils.normalizeString("UppERcaSE"), 'uppercase')

    def testNormalizeStringStrip(self):
        # Punctuation and spaces are trimmed, multiples reduced to 1
        self.assertEqual(self.utils.normalizeString(" a string    "),
                         'a-string')
        self.assertEqual(self.utils.normalizeString(">here's another!"),
                         'here-s-another')
        self.assertEqual(self.utils.normalizeString("one with !@#$!@#$ stuff in the middle"),
                         'one-with-stuff-in-the-middle')

    def testNormalizeStringFileExtensions(self):
        # If there is something that looks like a file extensions
        # it will be preserved.
        self.assertEqual(self.utils.normalizeString("this is a file.gif"),
                         'this-is-a-file.gif')
        self.assertEqual(self.utils.normalizeString("this is. also. a file.html"),
                         'this-is-also-a-file.html')

    def testNormalizeStringAccents(self):
        # European accented chars will be transliterated to rough ASCII equivalents
        input = u"Eksempel \xe6\xf8\xe5 norsk \xc6\xd8\xc5"
        self.assertEqual(self.utils.normalizeString(input),
                         'eksempel-eoa-norsk-eoa')

    def testNormalizeStringUTF8(self):
        # In real life, input will not be Unicode...
        input = u"Eksempel \xe6\xf8\xe5 norsk \xc6\xd8\xc5".encode('utf-8')
        self.assertEqual(self.utils.normalizeString(input),
                         'eksempel-eoa-norsk-eoa')

    def testNormalizeGreek(self):
        # Greek letters (not supported by UnicodeData)
        input = u'\u039d\u03af\u03ba\u03bf\u03c2 \u03a4\u03b6\u03ac\u03bd\u03bf\u03c2'
        self.assertEqual(self.utils.normalizeString(input), 'nikos-tzanos')

    def testNormalizeGreekUTF8(self):
        # Greek letters (not supported by UnicodeData)
        input = u'\u039d\u03af\u03ba\u03bf\u03c2 \u03a4\u03b6\u03ac\u03bd\u03bf\u03c2'.encode('utf-8')
        self.assertEqual(self.utils.normalizeString(input), 'nikos-tzanos')

    def testNormalizeStringHex(self):
        # Everything that can't be transliterated will be hex'd
        self.assertEqual(self.utils.normalizeString(u"\u9ad8\u8054\u5408 Chinese"),
                         '9ad880545408-chinese')
        self.assertEqual(self.utils.normalizeString(u"\uc774\ubbf8\uc9f1 Korean"),
                         'c774bbf8c9f1-korean')

    def testNormalizeStringObject(self):
        # Objects should be converted to strings using repr()
        self.assertEqual(self.utils.normalizeString(None), 'none')
        self.assertEqual(self.utils.normalizeString(True), 'true')
        self.assertEqual(self.utils.normalizeString(False), 'false')

class TestNavTree(PloneTestCase.PloneTestCase):
    '''Tests for the new navigation tree and sitemap'''

    def afterSetUp(self):
        from Products.LinguaPlone.Extensions.Install import setupPlone20Compat
        self.utils = self.portal.plone_utils
        self.populateSite()

        setupPlone20Compat(self.portal, StringIO())

    def populateSite(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document', 'doc1')
        self.portal.invokeFactory('Document', 'doc2')
        self.portal.invokeFactory('Document', 'doc3')
        self.portal.invokeFactory('Folder', 'folder1')
        folder1 = getattr(self.portal, 'folder1')
        folder1.invokeFactory('Document', 'doc11')
        folder1.invokeFactory('Document', 'doc12')
        folder1.invokeFactory('Document', 'doc13')
        self.portal.invokeFactory('Folder', 'folder2')
        folder2 = getattr(self.portal, 'folder2')
        folder2.invokeFactory('Document', 'doc21')
        folder2.invokeFactory('Document', 'doc22')
        folder2.invokeFactory('Document', 'doc23')
        folder2.invokeFactory('File', 'file21')
        self.setRoles(['Member'])

    def testTypesToList(self):
        # Make sure typesToList() returns the expected types
        wl = self.utils.typesToList()
        self.failUnless('Folder' in wl)
        self.failUnless('Large Plone Folder' in wl)
        self.failUnless('Topic' in wl)
        self.failIf('ATReferenceCriterion' in wl)

    def testCreateNavTree(self):
        # See if we can create one at all
        tree = self.utils.createNavTree(self.portal)
        self.failUnless(tree, tree)
        self.failUnless('children' in tree)

    def testCreateNavTreeCurrentItem(self):
        # With the context set to folder2 it should return a dict with
        # currentItem set to True
        tree = self.utils.createNavTree(self.portal.folder2)
        self.failUnless(tree, tree)
        self.assertEqual(tree['children'][-1]['currentItem'], True)

    def testCreateNavTreeRespectsTypesWithViewAction(self):
        # With a File or Image as current action it should return a
        # currentItem which has '/view' appended to the url
        tree = self.utils.createNavTree(self.portal.folder2.file21)
        self.failUnless(tree, tree)
        # Fail if 'view' is used for parent folder; it should only be on the File
        self.failIf(tree['children'][-1]['absolute_url'][-5:]=='/view')
        # Verify we have the correct object and it is the current item
        self.assertEqual(tree['children'][-1]['children'][-1]['currentItem'],True)
        self.assertEqual(tree['children'][-1]['children'][-1]['path'].split('/')[-1],'file21')
        # Verify that we have '/view'
        self.assertEqual(tree['children'][-1]['children'][-1]['absolute_url'][-5:],'/view')

    def testNavTreeExcludesItemsInIdsNotToList(self):
        # Make sure that items whose ids are in the idsNotToList navTree
        # property get no_display set to True
        ntp=self.portal.portal_properties.navtree_properties
        ntp.manage_changeProperties(idsNotToList=['folder2'])
        tree = self.utils.createNavTree(self.portal.folder2.file21)
        self.failUnless(tree, tree)
        self.assertEqual(tree['children'][-1]['no_display'],True)
        # Shouldn't exlude anything else
        self.assertEqual(tree['children'][0]['no_display'],False)

    def testNavTreeMarksParentMetaTypesNotToQuery(self):
        # Make sure that items whose ids are in the idsNotToList navTree
        # property get no_display set to True
        tree = self.utils.createNavTree(self.portal.folder2.file21)
        items = tree['children']
        self.failUnless(items[-1]['show_children'] == True, items)
        ntp=self.portal.portal_properties.navtree_properties
        ntp.manage_changeProperties(parentMetaTypesNotToQuery=['Folder'])
        tree = self.utils.createNavTree(self.portal.folder2.file21)
        items = tree['children']
        self.failUnless(items[-1]['show_children'] == False, items)

    def testCustomQuery(self):
        # Try a custom query script for the navtree that returns only published
        # objects
        workflow = self.portal.portal_workflow
        factory = self.portal.manage_addProduct['PythonScripts']
        factory.manage_addPythonScript('getCustomNavQuery')
        script = self.portal.getCustomNavQuery
        script.ZPythonScript_edit('','return {"review_state":"published"}')
        self.assertEqual(self.portal.getCustomNavQuery(),
                         {"review_state":"published"})
        tree = self.utils.createNavTree(self.portal.folder2)
        self.failUnless(tree, tree)
        self.failUnless('children' in tree)
        #Should only contain current object
        self.assertEqual(len(tree['children']), 1)
        #change workflow for folder1
        workflow.doActionFor(self.portal.folder1, 'publish')
        self.portal.folder1.reindexObject()
        tree = self.utils.createNavTree(self.portal.folder2)
        #Should only contain current object and published folder
        self.assertEqual(len(tree['children']), 2)

    def testStateFiltering(self):
        # Test Navtree workflow state filtering
        workflow = self.portal.portal_workflow
        ntp=self.portal.portal_properties.navtree_properties
        ntp.manage_changeProperties(wf_states_to_show=['published'])
        ntp.manage_changeProperties(enable_wf_state_filtering=True)
        tree = self.utils.createNavTree(self.portal.folder2)
        self.failUnless(tree, tree)
        self.failUnless('children' in tree)
        #Should only contain current object
        self.assertEqual(len(tree['children']), 1)
        #change workflow for folder1
        workflow.doActionFor(self.portal.folder1, 'publish')
        self.portal.folder1.reindexObject()
        tree = self.utils.createNavTree(self.portal.folder2)
        #Should only contain current object and published folder
        self.assertEqual(len(tree['children']), 2)

class TestIDGenerationMethods(PloneTestCase.PloneTestCase):
    '''Tests the isIDAutoGenerated method and pretty_title_or_id'''

    def afterSetUp(self):
        self.utils = self.portal.plone_utils

    def testAutoGeneratedId(self):
        r = self.utils.isIDAutoGenerated('document.2004-11-09.0123456789')
        self.assertEqual(r, True)

    def testValidPortalTypeNameButNotAutoGeneratedId(self):
        # This was raising an IndexError exception for
        # Zope < 2.7.3 (DateTime.py < 1.85.12.11) and a
        # SyntaxError for Zope >= 2.7.3 (DateTime.py >= 1.85.12.11)
        r = self.utils.isIDAutoGenerated('document.tar.gz')
        self.assertEqual(r, False)
        r = self.utils.isIDAutoGenerated('document.tar.12/32/2004')
        self.assertEqual(r, False)
        r = self.utils.isIDAutoGenerated('document.tar.12/31/2004 12:62')
        self.assertEqual(r, False)

    def test_pretty_title_or_id_returns_title(self):
        self.folder.setTitle('My pretty title')
        self.assertEqual(self.utils.pretty_title_or_id(self.folder), 'My pretty title')

    def test_pretty_title_or_id_returns_id(self):
        self.folder.setTitle('')
        self.assertEqual(self.utils.pretty_title_or_id(self.folder), self.folder.getId())

    def test_pretty_title_or_id_when_autogenerated(self):
        self.setRoles(['Manager','Member'])
        self.folder.setTitle('')
        self.folder._setId('folder.2004-11-09.0123456789')
        self.assertEqual(self.utils.pretty_title_or_id(self.folder),
                         self.utils.getEmptyTitle())
        self.assertEqual(self.utils.pretty_title_or_id(self.folder, 'Marker'),
                                'Marker')

    def test_pretty_title_or_id_works_with_method_that_needs_context(self):
        self.setRoles(['Manager','Member'])
        # Create a dummy class that looks at it's context to find the title
        new_obj = DummyTitle()
        new_obj = new_obj.__of__(self.folder)
        try:
            title = self.utils.pretty_title_or_id(new_obj)
        except AttributeError, e:
            self.fail('pretty_title_or_id failed to include context %s'%e)
        self.assertEqual(title, 'portal_catalog')

    def test_pretty_title_or_id_on_catalog_brain(self):
        cat = self.portal.portal_catalog
        self.setRoles(['Manager','Member'])
        self.folder.edit(title='My pretty title', description='foobar')
        results = cat(Description='foobar')
        self.assertEqual(len(results), 1)
        self.assertEqual(self.utils.pretty_title_or_id(results[0]),
                                                        'My pretty title')

    def test_pretty_title_or_id_on_catalog_brain_returns_id(self):
        cat = self.portal.portal_catalog
        self.setRoles(['Manager','Member'])
        self.folder.edit(title='', description='foobar')
        results = cat(Description='foobar')
        self.assertEqual(len(results), 1)
        self.assertEqual(self.utils.pretty_title_or_id(results[0]),
                                                        self.folder.getId())

    def test_pretty_title_or_id_on_catalog_brain_autogenerated(self):
        cat = self.portal.portal_catalog
        self.setRoles(['Manager','Member'])
        self.folder._setId('folder.2004-11-09.0123456789')
        self.folder.edit(title='',
                         description='foobar')
        results = cat(Description='foobar')
        self.assertEqual(len(results), 1)
        self.assertEqual(self.utils.pretty_title_or_id(results[0], 'Marker'),
                                                        'Marker')

    def test_pretty_title_or_id_on_catalog_brain_no_title(self):
        cat = self.portal.portal_catalog
        self.setRoles(['Manager','Member'])
        # Remove Title from catalog metadata to simulate a catalog with no
        # Title metadata and similar pathological cases.
        cat.delColumn('Title')
        self.folder.edit(title='', description='foobar')
        results = cat(Description='foobar')
        self.assertEqual(len(results), 1)
        # Give the portal a title because this is what will show up on
        # failure
        self.portal.title = 'This is not the title you are looking for'
        self.assertEqual(self.utils.pretty_title_or_id(results[0]),
                                                        self.folder.getId())

def test_suite():
    from unittest import TestSuite
    suite = TestSuite()
    return suite
