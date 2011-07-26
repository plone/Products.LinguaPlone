from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.interfaces import ITranslatable
from Products.LinguaPlone.tests import dummy
from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation


class TestLanguageIndependentFields(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.addLanguage('fr')
        self.addLanguage('it')
        self.setLanguage('en')

    def testLanguageIndependentField(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')

        contact = 'Fred Flintstone'
        english.setContactName(contact)
        german = makeTranslation(english, 'de')
        self.assertEqual(english.getContactName(), contact)
        self.assertEqual(english.getRawContactName(), contact)
        self.assertEqual(german.getContactName(), contact)
        self.assertEqual(german.getRawContactName(), contact)
        self.failUnless(english.contactName)
        self.failUnless(german.contactName)
        self.failUnless(hasattr(german, 'testing'))
        self.assertEqual(german.testing, english.contactName)
        self.assertEqual(english.contactName, german.contactName)

        contact = 'Barney Rubble'
        german.setContactName(contact)
        self.assertEqual(english.getContactName(), contact)
        self.assertEqual(english.getRawContactName(), contact)
        self.assertEqual(german.getContactName(), contact)
        self.assertEqual(german.getRawContactName(), contact)
        self.failUnless(english.contactName)
        self.failUnless(german.contactName)
        self.failUnless(hasattr(english, 'testing'))
        self.assertEqual(english.testing, german.contactName)
        self.assertEqual(english.contactName, german.contactName)

        # Sanity check: not all fields are language independent
        english.setTitle('English title')
        german.setTitle('German title')
        self.failIfEqual(english.Title(), german.Title())

    def test_textfield(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        english.setNeutralText('<p>Hello</p>')
        self.assertEqual(english.neutralText.getContentType(), 'text/html')
        german = makeTranslation(english, 'de')
        text = german.getNeutralText()
        self.assertEqual(text, '<p>Hello</p>')
        self.assertEqual(german.neutralText.getContentType(), 'text/html')

    def test_textfield_empty_update(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        english.setNeutralText('')
        self.assertEqual(english.neutralText.getContentType(), 'text/plain')
        german = makeTranslation(english, 'de')
        self.assertEqual(german.getNeutralText(), '')
        self.assertEqual(german.neutralText.getContentType(), 'text/plain')
        # update field
        english.setNeutralText('<p>Hello</p>')
        self.assertEqual(english.neutralText.getContentType(), 'text/html')
        self.assertEqual(german.getNeutralText(), '<p>Hello</p>')
        self.assertEqual(german.neutralText.getContentType(), 'text/html')

    def test_textfield_on_document(self):
        from Products.LinguaPlone.utils import LanguageIndependentFields
        english = makeContent(self.folder, 'Document', 'doc')
        english.setLanguage('en')
        english.setText('')
        key = 'Archetypes.storage.AnnotationStorage-text'
        baseunit = english.__annotations__[key]
        self.assertEqual(baseunit.getContentType(), 'text/plain')
        # use the LanguageIndependentFields adapter to copy the text field
        def getFields(self, schema=None):
            if schema is None:
                schema = self.context.Schema()
            return schema.filterFields(__name__='text')
        orig = LanguageIndependentFields.getFields
        try:
            LanguageIndependentFields.getFields = getFields
            german = makeTranslation(english, 'de')
            self.assertEqual(german.getText(), '')
            de_baseunit = german.__annotations__[key]
            self.assertEqual(de_baseunit.getContentType(), 'text/plain')
            # update field
            english.setText('<p>Hello</p>')
            LanguageIndependentFields(english).copyFields(german)
            self.assertEqual(baseunit.getContentType(), 'text/html')
            self.assertEqual(german.getText(), '<p>Hello</p>')
            self.assertEqual(de_baseunit.getContentType(), 'text/html')
        finally:
            LanguageIndependentFields.getFields = orig

    def testLinesField(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')

        english.setLines(('foo', 'bar'))

        german = makeTranslation(english, 'de')
        self.assertEqual(german.getLines(), ('foo', 'bar'))

        english.setLines(('bar', 'baz'))
        self.assertEqual(german.getLines(), ('bar', 'baz'))

    def testReferenceFields(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')

        target = makeContent(self.folder, 'SimpleType', 'target')
        target.setLanguage('en')

        # Test language dependent reference fields
        english.setReferenceDependent(target.UID())
        self.assertEqual(english.getReferenceDependent().UID(), target.UID())
        self.assertEqual(german.getReferenceDependent(), None)

        # Test language independent reference fields
        english.setReference(target.UID())
        self.assertEqual(english.getReference().UID(), target.UID())
        self.assertEqual(german.getReference().UID(), target.UID())

        # Now we make a german translation of the target
        target_german = makeTranslation(target, 'de')

        # The language dependent field shouldn't change
        self.assertEqual(english.getReferenceDependent().UID(), target.UID())
        self.assertEqual(german.getReferenceDependent(), None)

        # It would be nice if the language independent field would now
        # point to the translation of the target, but this isn't easy to do
        # Neither the canonical or any translation of the content type with
        # the reference will actually be changed at this point. So we would
        # need to check on translation creation if the canonical is referenced
        # by any item and update those. This is a potential performance
        # nightmare, so we won't do it now
        self.assertEqual(english.getReference().UID(), target.UID())
        self.assertEqual(german.getReference().UID(), target.UID())

        # If we clear the reference, there should be no link left
        english.setReferenceDependent(None)
        english.setReference(None)

        self.assertEqual(english.getReferenceDependent(), None)
        self.assertEqual(german.getReferenceDependent(), None)

        self.assertEqual(english.getReference(), None)
        self.assertEqual(german.getReference(), None)

        # If the target already has a translation, it should set the reference
        # to the translation right away

        target2 = makeContent(self.folder, 'SimpleType', 'target2')
        target2_german = makeTranslation(target2, 'de')

        english.setReferenceDependent(target2.UID())
        self.assertEqual(english.getReferenceDependent().UID(), target2.UID())
        self.assertEqual(german.getReferenceDependent(), None)

        english.setReference(target2.UID())
        self.assertEqual(english.getReference().UID(), target2.UID())
        self.assertEqual(german.getReference().UID(), target2_german.UID())

        # If we delete the referenced item, it should no longer be referenced
        self.folder._delObject(target_german.getId())
        self.folder._delObject(target.getId())
        self.folder._delObject(target2_german.getId())
        self.folder._delObject(target2.getId())

        self.assertEqual(english.getReferenceDependent(), None)
        self.assertEqual(german.getReferenceDependent(), None)

        self.assertEqual(english.getReference(), None)
        self.assertEqual(german.getReference(), None)

    def testMultiValuedReferenceFields(self):
        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')

        target = makeContent(self.folder, 'SimpleType', 'target')
        target.setLanguage('en')
        target_german = makeTranslation(target, 'de')

        target2 = makeContent(self.folder, 'SimpleType', 'target2')
        target2.setLanguage('en')
        target2_german = makeTranslation(target2, 'de')

        # untranslated target
        target3 = makeContent(self.folder, 'SimpleType', 'target3')
        target3.setLanguage('en')

        # targets with different language than sources
        target4 = makeContent(self.folder, 'SimpleType', 'target4')
        target4.setLanguage('fr')
        target4_italian = makeTranslation(target4, 'it')

        # untranslatable target (non-LP aware)
        target5 = makeContent(self.folder, 'UntranslatableType', 'target5')
        self.assertEqual(ITranslatable.providedBy(target5), False)

        # Test single valued
        english.setReferenceMulti(target.UID())
        self.assertEqual(english.getReferenceMulti()[0].UID(), target.UID())
        self.assertEqual(german.getReferenceMulti()[0].UID(),
            target_german.UID())

        # Test multi-valued
        english.setReferenceMulti([target.UID(), target2.UID()])
        self.assertEqual(set(english.getReferenceMulti()),
            set([target, target2]))
        self.assertEqual(set(german.getReferenceMulti()),
            set([target_german, target2_german]))

        # Test multi-valued from tuple
        english.setReferenceMulti((target.UID(), target2.UID()))
        self.assertEqual(set(english.getReferenceMulti()),
            set([target, target2]))
        self.assertEqual(set(german.getReferenceMulti()),
            set([target_german, target2_german]))

        # test reduce references
        english.setReferenceMulti([target.UID()])
        self.assertEqual(len(english.getReferenceMulti()), 1)

        # test delete references
        english.setReferenceMulti([])
        self.assertEqual(len(english.getReferenceMulti()), 0)

        # test with untranslated target, german points to only canonical target
        english.setReferenceMulti([target3.UID()])
        self.assertEqual(english.getReferenceMulti()[0].UID(), target3.UID())
        self.assertEqual(german.getReferenceMulti()[0].UID(), target3.UID())

        # test with an untranslatable target
        english.setReferenceMulti([target5.UID()])
        self.assertEqual(english.getReferenceMulti()[0].UID(), target5.UID())
        self.assertEqual(german.getReferenceMulti()[0].UID(), target5.UID())

        # test with untranslatable and translatable mixed targets
        english.setReferenceMulti([target.UID(), target5.UID()])
        self.assertEqual(set(english.getReferenceMulti()),
            set([target, target5]))
        self.assertEqual(set(german.getReferenceMulti()),
            set([target_german, target5]))

        # test remove translatable from the list
        english.setReferenceMulti([target5.UID()])
        self.assertEqual(english.getReferenceMulti()[0].UID(), target5.UID())
        self.assertEqual(german.getReferenceMulti()[0].UID(), target5.UID())

        # test with different language on targets, "fr" is canonical
        english.setReferenceMulti([target4.UID()])
        self.assertEqual(english.getReferenceMulti()[0].UID(), target4.UID())
        self.assertEqual(german.getReferenceMulti()[0].UID(), target4.UID())

        # after adding an italian content, it must point to italian target
        italian = makeTranslation(english, 'it')
        self.assertEqual(italian.getReferenceMulti()[0].UID(),
                         target4_italian.UID())

        # test edge cases, can we use None to delete references?
        english.setReferenceMulti(None)

        # can we delete things via an empty string?
        english.setReferenceMulti([target2])
        english.setReferenceMulti('')
        self.failUnless(len(english.getReferenceMulti()) == 0)

        english.setReferenceMulti([target2])
        english.setReferenceMulti([''])
        self.failUnless(len(english.getReferenceMulti()) == 0)

        # can we use a content object instead of its UID?
        english.setReferenceMulti([target2])
        self.assertEqual(english.getReferenceMulti()[0].UID(), target2.UID())
        self.assertEqual(
            german.getReferenceMulti()[0].UID(), target2_german.UID())

    def testBaseSchemaSetup(self):
        schema = dummy.SimpleType.schema
        self.assertEqual(
            schema['langIndependentInBase'].languageIndependent, 1)
        self.assertEqual(
            schema['langIndependentInDerived'].languageIndependent, 0)
        self.assertEqual(
            schema['langIndependentInBoth'].languageIndependent, 1)

    def testDerivedSchemaSetup(self):
        schema = dummy.DerivedType.schema
        self.assertEqual(
            schema['langIndependentInBase'].languageIndependent, 0)
        self.assertEqual(
            schema['langIndependentInDerived'].languageIndependent, 1)
        self.assertEqual(
            schema['langIndependentInBoth'].languageIndependent, 1)

    def testLangIndependentInBase(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        teststring = 'Test string'
        # When overriding languageIndependent from base class, the original
        # translation aware mutator actually checks for language independence
        english.setLangIndependentInBase(teststring)
        self.failIfEqual(german.getLangIndependentInBase(), teststring)
        self.failIfEqual(german.getRawLangIndependentInBase(), teststring)

    def testLangIndependentInDerived(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        teststring = 'Test string'
        # Note that you *can* override a 'false' languageIndependent field
        # from a base class...
        english.setLangIndependentInDerived(teststring)
        self.assertEqual(german.getLangIndependentInDerived(), teststring)
        self.assertEqual(german.getRawLangIndependentInDerived(), teststring)

    def testLangIndependentInBoth(self):
        english = makeContent(self.folder, 'DerivedType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')
        teststring = 'Test string'
        english.setLangIndependentInBoth(teststring)
        self.assertEqual(german.getLangIndependentInBoth(), teststring)
        self.assertEqual(german.getRawLangIndependentInBoth(), teststring)

    # Test content that is not LP-aware
    def testLangIndependentGeneratedMethodsInNonLP(self):
        english = makeContent(self.folder, 'NonLPSimpleType', 'doc')
        english.setLanguage('en')
        teststring = 'Test string'
        # If this fails, you can't inherit unless you also get a copy
        # of the schema
        english.setLangIndependentInBase(teststring)
        self.assertEqual(english.getLangIndependentInBase(), teststring)
        self.assertEqual(english.getRawLangIndependentInBase(), teststring)

    def testNotLangIndependentCustomMethodsInNonLP(self):
        english = makeContent(self.folder, 'NonLPSimpleType', 'doc')
        english.setLanguage('en')
        teststring = 'Test string'
        # If this fails, you can't inherit unless you also get a copy
        # of the schema
        english.setFourthContactName(teststring)
        self.assertEqual(english.getFourthContactName(),
                         'getFourthContactName')
        self.assertEqual(str(english.contactName4), 'cn4 %s' % teststring)

    def testLangIndependentCustomMethodsInNonLP(self):
        english = makeContent(self.folder, 'NonLPSimpleType', 'doc')
        english.setLanguage('en')
        teststring = 'Test string'
        # If this fails, you can't inherit unless you also get a copy
        # of the schema
        english.setFifthContactName(teststring)
        self.assertEqual(english.getFifthContactName(), 'getFifthContactName')
        # The original method is not detected properly... annotate?
        # Annotate the generated method!!!! provide original method name
        self.assertEqual(str(english.contactName5), 'cn5 %s' % teststring)


class TestLanguageIndependentCatalog(LinguaPloneTestCase):

    def afterSetUp(self):
        self.addLanguage('de')
        self.setLanguage('en')

    def testLangIndependentIndexing(self):
        catalog = getToolByName(self.folder, 'portal_catalog')
        catalog.addColumn('getContactName')

        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        english.processForm(values=dict(contactName='foo'))
        res = [r.getContactName for r in
            catalog(dict(portal_type='SimpleType', Language='en'))]
        self.assertEqual(res, ['foo'])

        makeTranslation(english, 'de')
        english.processForm(values=dict(contactName='bar'))

        brains = catalog(dict(portal_type='SimpleType', Language='en'))
        self.assertEqual(brains[0].getContactName, 'bar')
        brains = catalog(dict(portal_type='SimpleType', Language='de'))
        self.assertEqual(brains[0].getContactName, 'bar')

    def testLangIndependentReferenceIndexing(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        catalog.addIndex('getRawReference', 'FieldIndex')
        catalog.addColumn('getRawReference')

        catalog.addIndex('getRawReferenceDependent', 'FieldIndex')
        catalog.addColumn('getRawReferenceDependent')

        english = makeContent(self.folder, 'SimpleType', 'doc')
        english.setLanguage('en')
        german = makeTranslation(english, 'de')

        target = makeContent(self.folder, 'SimpleType', 'target')
        target.setLanguage('en')
        target_german = makeTranslation(target, 'de')

        # Test language independent reference fields
        english.processForm(values=dict(
            reference=target.UID(), referenceDependent=target.UID()))

        self.assertEqual(english.getReference().UID(), target.UID())
        self.assertEqual(german.getReference().UID(), target_german.UID())

        brains = catalog(dict(getRawReferenceDependent=target.UID()))
        self.assertEqual(brains[0].getRawReferenceDependent, target.UID())
        brains = catalog(dict(getRawReferenceDependent=target.UID()))
        self.assertEqual(brains[0].getRawReferenceDependent, target.UID())

        brains = catalog(dict(UID=english.UID()))
        self.assertEqual(brains[0].getRawReference, target.UID())
        brains = catalog(dict(UID=german.UID()))
        self.assertEqual(brains[0].getRawReference, target_german.UID())
