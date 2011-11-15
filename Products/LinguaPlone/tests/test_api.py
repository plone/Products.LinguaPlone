import transaction

from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.public import AlreadyTranslated
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


def sortTuple(t):
    l = list(t)
    l.sort()
    return tuple(l)


class TestAPI(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('fr')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.alsoenglish = makeContent(self.folder, 'SimpleType', 'doctwo')
        self.alsoenglish.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')
        self.french = makeContent(self.folder, 'SimpleType', 'frenchdoc')
        self.french.setLanguage('fr')
        self.folder_en = makeContent(self.folder, 'SimpleFolder', 'folder')
        self.folder_en.setLanguage('en')

    def testEnglishIsCanonical(self):
        self.assertEqual(self.english.isCanonical(), True)

    def testEnglishIsTranslation(self):
        self.assertEqual(self.english.isTranslation(), True)

    def testGermanIsNotCanonical(self):
        self.assertEqual(self.german.isCanonical(), False)

    def testGermanIsTranslation(self):
        self.assertEqual(self.german.isTranslation(), True)

    def testGetCanonicalFromCanonicalObject(self):
        self.assertEqual(self.english, self.english.getCanonical())

    def testGetCanonicalFromNonCanonicalObject(self):
        self.assertEqual(self.english, self.german.getCanonical())

    def testCanonicalGetLanguage(self):
        self.assertEqual(self.english.getLanguage(), 'en')

    def testNonCanonicalGetLanguage(self):
        self.assertEqual(self.german.getLanguage(), 'de')

    def testCanonicalHasTranslationForEnglish(self):
        self.failUnless(self.english.hasTranslation('en'))

    def testCanonicalHasTranslationForGerman(self):
        self.failUnless(self.english.hasTranslation('de'))

    def testCanonicalHasNoTranslationForFrench(self):
        self.failIf(self.english.hasTranslation('fr'))

    def testNonCanonicalHasTranslationForEnglish(self):
        self.failUnless(self.german.hasTranslation('en'))

    def testNonCanonicalHasTranslationForGerman(self):
        self.failUnless(self.german.hasTranslation('de'))

    def testNonCanonicalHasNoTranslationForFrench(self):
        self.failIf(self.german.hasTranslation('fr'))

    def testSchemaUpdateDoesNotRaiseAlreadyTranslated(self):
        # Actually, this passes even with the original wrong code,
        # because the AlreadyTranslated exception gets swallowed
        # somewhere.  In the browser it does not get swallowed, but
        # gives a real error for any language that is not the default.
        self.english._updateSchema()
        self.german._updateSchema()
        self.french._updateSchema()

    def testCanonicalSetLanguageRaiseAlreadyTranslated(self):
        self.assertRaises(AlreadyTranslated, self.english.setLanguage, 'de')

    def testNonCanonicalSetLanguageRaiseAlreadyTranslated(self):
        self.assertRaises(AlreadyTranslated, self.german.setLanguage, 'en')

    def testCanonicalAddTranslationReferenceRaiseAlreadyTranslated(self):
        self.assertRaises(AlreadyTranslated,
                self.english.addTranslationReference, self.english)
        self.assertRaises(AlreadyTranslated,
                self.english.addTranslationReference, self.alsoenglish)

    def testCanonicalAddTranslationRaiseAlreadyTranslated(self):
        self.assertRaises(AlreadyTranslated, self.english.addTranslation, 'en')

    def testNonCanonicalAddTranslationRaiseAlreadyTranslated(self):
        self.assertRaises(AlreadyTranslated, self.german.addTranslation, 'en')

    def testMakeTranslationCreateDifferentObjects(self):
        self.failIfEqual(self.english, self.german)

    def testMakeTranslationCreateSecondTranslation(self):
        self.french = makeTranslation(self.english, 'fr')
        self.failIfEqual(self.english, self.french)
        self.failIfEqual(self.german, self.french)
        self.assertEqual(self.french.getLanguage(), 'fr')

    def testGetCanonicalLanguageFromCanonicalObject(self):
        self.assertEqual('en', self.english.getCanonicalLanguage())

    def testGetCanonicalLanguageFromNonCanonicalObject(self):
        self.assertEqual('en', self.german.getCanonicalLanguage())

    def testGetTranslationReturnsDefault(self):
        self.assertEqual(self.english, self.german.getTranslation())

    def testGetTranslationWithoutLanguageTool(self):
        self.loginAsPortalOwner()
        del self.portal['portal_languages']
        self.assertEqual(self.german, self.german.getTranslation())

    def testGetTranslationFromCanonicalReturnLanguageObject(self):
        self.assertEqual(self.german, self.english.getTranslation('de'))

    def testGetTranslationFromNonCanonicalReturnLanguageObject(self):
        self.assertEqual(self.german, self.german.getTranslation('de'))

    def testGetTranslationWithMultipleLanguages(self):
        self.french = makeTranslation(self.german, 'fr')
        self.assertEqual(self.french, self.german.getTranslation('fr'))
        self.assertEqual(self.french, self.english.getTranslation('fr'))
        self.assertEqual(self.german, self.french.getTranslation('de'))
        self.assertEqual(self.german, self.english.getTranslation('de'))
        self.assertEqual(self.english, self.german.getTranslation('en'))
        self.assertEqual(self.english, self.french.getTranslation('en'))

    def testChangeCanonical(self):
        self.german.setCanonical()
        self.failIf(self.english.isCanonical())
        self.failUnless(self.german.isCanonical())
        self.assertEqual('de', self.english.getCanonicalLanguage())
        self.assertEqual('de', self.german.getCanonicalLanguage())
        self.assertEqual(self.german, self.english.getCanonical())
        self.assertEqual(self.german, self.german.getCanonical())
        self.french = makeTranslation(self.german, 'fr')
        self.french.setCanonical()
        self.failIf(self.english.isCanonical())
        self.failIf(self.german.isCanonical())
        self.failUnless(self.french.isCanonical())
        self.assertEqual('fr', self.english.getCanonicalLanguage())
        self.assertEqual('fr', self.french.getCanonicalLanguage())
        self.assertEqual('fr', self.german.getCanonicalLanguage())
        self.assertEqual(self.french, self.english.getCanonical())
        self.assertEqual(self.french, self.french.getCanonical())
        self.assertEqual(self.french, self.german.getCanonical())
        self.english.setCanonical()
        self.failUnless(self.english.isCanonical())
        self.failIf(self.german.isCanonical())
        self.failIf(self.french.isCanonical())
        self.assertEqual('en', self.english.getCanonicalLanguage())
        self.assertEqual('en', self.french.getCanonicalLanguage())
        self.assertEqual('en', self.german.getCanonicalLanguage())
        self.assertEqual(self.english, self.english.getCanonical())
        self.assertEqual(self.english, self.french.getCanonical())
        self.assertEqual(self.english, self.german.getCanonical())

    def testGetTranslationLanguages(self):
        languages = self.english.getTranslationLanguages()
        self.assertEqual(sortTuple(('en', 'de')), sortTuple(languages))

    def testGetTranslations(self):
        translations = self.english.getTranslations()
        self.assertEqual(translations['en'][0], self.english)
        self.assertEqual(translations['en'][1], 'private')
        self.assertEqual(translations['de'][0], self.german)
        self.assertEqual(translations['de'][1], 'private')

    def testGetTranslationsNoWorkflowToolNoReviewState(self):
        self.loginAsPortalOwner()
        del self.portal['portal_workflow']
        translations = self.english.getTranslations()
        self.assertEqual(translations['en'][0], self.english)
        self.assertEqual(translations['en'][1], None)

    def testGetTranslationsNoReviewState(self):
        translations = self.english.getTranslations(review_state=False)
        self.assertEqual(translations['en'], self.english)
        self.assertEqual(translations['de'], self.german)

    def testGetTranslationsNoWorkflowTool(self):
        self.loginAsPortalOwner()
        del self.portal['portal_workflow']
        translations = self.english.getTranslations(review_state=False)
        self.assertEqual(translations['en'], self.english)

    def testGetTranslationsMissingObject(self):
        french = makeTranslation(self.german, 'fr')
        translations = self.english.getTranslations(review_state=False)
        self.assertEqual(translations['fr'], french)
        self.loginAsPortalOwner()
        self.folder._delOb(french.getId())
        translations = self.english.getTranslations(review_state=False)
        self.assert_('fr' not in translations)

    def testGetNonCanonicalTranslations(self):
        translations = self.english.getNonCanonicalTranslations()
        self.assertEquals(len(translations), 1)
        self.assertEqual(translations['de'][0], self.german)
        self.assertEqual(translations['de'][1], 'private')

    def testReferences(self):
        reftool = self.portal.reference_catalog
        ref = reftool.getReferences(self.german, 'translationOf')[0]
        self.assertEqual(self.german, ref.getSourceObject())
        self.assertEqual(self.english, ref.getTargetObject())
        self.assertEqual(self.german,
                         self.english.getBRefs('translationOf')[0])
        self.assertEqual(self.english,
                         self.german.getRefs('translationOf')[0])

    def testGetTranslationReferences(self):
        refs = self.german.getTranslationReferences()
        self.assertEquals(len(refs), 1)
        trans = self.german.getTranslationReferences(objects=True)
        self.assertEquals(trans[0], self.english)

    def testRenameTranslation(self):
        transaction.savepoint(optimistic=True)
        self.folder.manage_renameObject(self.german.getId(), 'foo')
        self.failUnless('de' in self.english.getTranslationLanguages())
        self.assertEqual(self.english.getTranslation('de').getId(), 'foo')

    def testCanonicalInvalidateTranslations(self):
        self.english.invalidateTranslations()
        self.failIf(self.english.isOutdated())
        self.failUnless(self.german.isOutdated())

    def testTranslationInvalidateTranslations(self):
        self.german.invalidateTranslations()
        self.failIf(self.english.isOutdated())
        self.failUnless(self.german.isOutdated())

    def testRemoveTranslationNonCanonical(self):
        self.english.removeTranslation('de')
        self.failIf(self.english.getTranslation('de'))

    def testRemoveTranslationCanonical(self):
        self.french = makeTranslation(self.english, 'fr')
        self.german.removeTranslation('en')
        # German becomes the new Canonical
        self.failUnless(self.german.isCanonical())
        self.failIf(self.french.isCanonical())
        self.failIf(self.german.getTranslation('en'))
        self.failIf(self.french.getTranslation('en'))
        self.failUnless(self.german.getTranslation('fr'))

    def testProcessFormNotifyTranslations(self):
        self.failIf(self.german.isOutdated())
        self.english.processForm(values={'title': 'English'})
        self.failUnless(self.german.isOutdated())
        self.german.processForm(values={'title': 'German'})
        self.failIf(self.german.isOutdated())
        self.failIf(self.english.isOutdated())

    def testUnlinkTranslation(self):
        de = self.english.getTranslation('de')
        self.english.removeTranslationReference(de)
        self.failIf(self.english.hasTranslation('de'))
        self.assert_(de.getId() in self.folder)

    def testDefaultLanguage(self):
        de_folder = makeContent(self.folder, 'SimpleFolder', 'de')
        de_folder.setLanguage('de')
        de_doc = makeContent(de_folder, 'SimpleType', 'doc-de')
        self.assertEquals(de_doc.defaultLanguage(), 'de')

    def testDefaultLanguageNeutralFolder(self):
        neutral_folder = makeContent(self.folder, 'SimpleFolder', 'neutral')
        neutral_folder.setLanguage('')
        neutral_doc = makeContent(neutral_folder, 'SimpleType', 'doc-neutral')
        # Adding content to a neutral folder defaults to it being neutral,
        # even if the site is not neutral by default
        self.assertEquals(neutral_doc.defaultLanguage(), '')

    def testDefaultLanguageNeutralSite(self):
        self.loginAsPortalOwner()
        ltool = getToolByName(self.portal, 'portal_languages')
        ltool.start_neutral = True
        neutral_folder = makeContent(self.folder, 'SimpleFolder', 'neutral')
        neutral_folder.setLanguage('')
        neutral_doc = makeContent(neutral_folder, 'SimpleType', 'doc-neutral')
        self.assertEquals(neutral_doc.defaultLanguage(), '')

    def testDefaultLanguageNonNeutralSite(self):
        self.loginAsPortalOwner()
        ltool = getToolByName(self.portal, 'portal_languages')
        ltool.start_neutral = False
        neutral_folder = makeContent(self.folder, 'SimpleFolder', 'neutral')
        neutral_folder.setLanguage('')
        neutral_doc = makeContent(neutral_folder, 'SimpleType', 'doc-neutral')
        self.assertEquals(neutral_doc.defaultLanguage(), '')

    def testDefaultLanguageNoLanguageTool(self):
        neutral_folder = makeContent(self.folder, 'SimpleFolder', 'neutral')
        neutral_folder.setLanguage('')
        neutral_doc = makeContent(neutral_folder, 'SimpleType', 'doc-neutral')
        self.loginAsPortalOwner()
        del self.portal['portal_languages']
        from Products.Archetypes.config import LANGUAGE_DEFAULT
        self.assertEquals(neutral_doc.defaultLanguage(), LANGUAGE_DEFAULT)


class TestSetLanguage(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('fr')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')

    def testCanonicalSetLanguage(self):
        self.english.setLanguage('fr')
        self.assertEqual(self.english.getLanguage(), 'fr')

    def testNonCanonicalSetLanguage(self):
        refs = self.german.getTranslationReferences()
        self.assertEqual(refs[0].Language, 'de')

        self.german.setLanguage('fr')
        self.assertEqual(self.german.getLanguage(), 'fr')
        refs = self.german.getTranslationReferences()
        self.assertEqual(refs[0].Language, 'fr')

    def testCanonicalSetLanguageAddFrenchCanonical(self):
        self.english.setLanguage('fr')
        self.failUnless('fr' in self.english.getTranslationLanguages())

    def testCanonicalSetLanguageRemoveEnglishCanonical(self):
        self.english.setLanguage('fr')
        self.failIf('en' in self.english.getTranslationLanguages())

    def testCanonicalSetLanguageAddFrenchNonCanonical(self):
        self.english.setLanguage('fr')
        self.failUnless('fr' in self.german.getTranslationLanguages())

    def testCanonicalSetLanguageRemoveEnglishNonCanonical(self):
        self.english.setLanguage('fr')
        self.failIf('en' in self.german.getTranslationLanguages())

    def testNonCanonicalSetLanguageAddFrenchCanonical(self):
        self.german.setLanguage('fr')
        self.failUnless('fr' in self.english.getTranslationLanguages())

    def testNonCanonicalSetLanguageRemoveEnglishCanonical(self):
        self.german.setLanguage('fr')
        self.failIf('de' in self.english.getTranslationLanguages())

    def testNonCanonicalSetLanguageAddFrenchNonCanonical(self):
        self.german.setLanguage('fr')
        self.failUnless('fr' in self.german.getTranslationLanguages())

    def testCanonicalSetLanguageToNeutral(self):
        self.english.setLanguage('')
        self.assertEqual(self.english.getLanguage(), '')

    def testNonCanonicalSetLanguageToNeutral(self):
        self.german.setLanguage('')
        self.assertEqual(self.german.getLanguage(), '')

    def testThreeLanguagesCanonicalSetLanguageToNeutral(self):
        self.french = makeTranslation(self.english, 'fr')
        self.english.setLanguage('')
        self.failIf('en' in self.english.getTranslationLanguages())
        self.failIf('fr' in self.english.getTranslationLanguages())
        self.failIf('de' in self.english.getTranslationLanguages())
        self.failIf('en' in self.french.getTranslationLanguages())
        self.failIf('en' in self.german.getTranslationLanguages())

    def testThreeLanguagesNonCanonicalSetLanguageToNeutral(self):
        self.french = makeTranslation(self.english, 'fr')
        self.german.setLanguage('')
        self.failIf('de' in self.german.getTranslationLanguages())
        self.failIf('en' in self.german.getTranslationLanguages())
        self.failIf('fr' in self.german.getTranslationLanguages())
        self.failIf('de' in self.english.getTranslationLanguages())
        self.failIf('de' in self.french.getTranslationLanguages())

    def testSchemaUpdatePreserveLanguage(self):
        self.failUnless('en' in self.german.getTranslationLanguages())
        self.german._updateSchema()
        self.failUnless('en' in self.german.getTranslationLanguages())


class TestProcessFormRename(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')
        self.english.setLanguage('en')
        self.german = makeTranslation(self.english, 'de')

    def testProcessFormIdFromTitleWithRequest(self):
        self.loginAsPortalOwner()
        self.addLanguage('fr')
        french = makeTranslation(self.english, 'fr')
        from zope.publisher.browser import TestRequest
        request = TestRequest(form={
                       'id': french.getId(),
                       'title': 'Biere'})
        french.processForm(REQUEST=request)
        self.assertNotEqual(french.getId(), 'doc-fr')
        self.assertEqual(french.getId(), 'biere')

    def testProcessFormIdFromTitleWithRequestSeparateFolder(self):
        self.en_folder = makeContent(self.folder, 'Folder', 'inner_folder')
        self.inner_english = makeContent(self.en_folder, 'SimpleType', 'doc')
        self.loginAsPortalOwner()
        self.addLanguage('fr')
        fr_folder = makeTranslation(self.en_folder, 'fr')
        french = makeTranslation(self.inner_english, 'fr')
        self.assertTrue(french.absolute_url().startswith(
            fr_folder.absolute_url()))
        from zope.publisher.browser import TestRequest
        request = TestRequest(form={
                       'id': french.getId(),
                       'title': 'Biere'})
        french.processForm(REQUEST=request)
        self.assertNotEqual(french.getId(), 'doc-fr')
        self.assertEqual(french.getId(), 'biere')

    def testProcessFormIdSetFromRequest(self):
        self.loginAsPortalOwner()
        self.addLanguage('fr')
        french = makeTranslation(self.english, 'fr')
        transaction.savepoint(optimistic=True)
        from zope.publisher.browser import TestRequest
        request = TestRequest(form={
                       'id': 'une-biere',
                       'title': 'Biere'})
        french.processForm(REQUEST=request)
        self.assertEqual(french.getId(), 'une-biere')

    def testProcessFormRenameObject(self):
        transaction.savepoint(optimistic=True)
        # Fake a auto generated ID
        self.english.setId(self.portal.generateUniqueId('SimpleType'))
        self.english.processForm(values={'title': 'I was renamed'})
        self.assertEqual(self.english.getId(), 'i-was-renamed')

    def testProcessFormRenameObjectOnlyFirstTime(self):
        transaction.savepoint(optimistic=True)
        # Fake a auto generated ID
        self.english.setId(self.portal.generateUniqueId('SimpleType'))
        self.english.processForm(values={'title': 'Only First'})
        self.english.processForm(values={'title': 'Not Second'})
        self.assertEqual(self.english.getId(), 'only-first')

    def testProcessFormRenamesTranslation(self):
        transaction.savepoint(optimistic=True)
        self.german.processForm(values={'title': 'Renamed Too'})
        self.assertEqual(self.german.getId(), 'renamed-too')

    def testProcessFormRenameTranslationWithId(self):
        transaction.savepoint(optimistic=True)
        self.german.processForm(values={'id': 'explicit-id'})
        self.german.processForm(values={'title': 'But not Title'})
        self.assertEqual(self.german.getId(), 'explicit-id')
