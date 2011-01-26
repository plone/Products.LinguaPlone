import os

from Products.LinguaPlone.tests.base import LinguaPloneTestCase
from Products.LinguaPlone.tests.utils import makeContent
from Products.LinguaPlone.tests.utils import makeTranslation

import Products.LinguaPlone.tests
filebase = os.path.join(Products.LinguaPlone.tests.__path__[0], 'red.')
PNG = file(filebase +'png').read()
JPG = file(filebase +'jpg').read()
GIF = file(filebase + 'gif').read()


class TestImage(LinguaPloneTestCase):

    def afterSetUp(self):
        self.setLanguage('en')
        self.addLanguage('de')
        self.english = makeContent(self.folder, 'SimpleType', 'doc')

    def testIndependentJPG(self):
        self.english.setImage(JPG)
        self.german = makeTranslation(self.english, 'de')
        img_en = self.english.getImage()
        img_de = self.german.getImage()
        self.failUnlessEqual(img_en.content_type, 'image/jpeg')
        self.failUnlessEqual(img_de.content_type, 'image/jpeg')

    def testIndependentPNG(self):
        self.english.setImage(PNG)
        self.german = makeTranslation(self.english, 'de')
        img_en = self.english.getImage()
        img_de = self.german.getImage()
        self.failUnlessEqual(img_en.content_type, 'image/png')
        self.failUnlessEqual(img_de.content_type, 'image/png')

    def testIndependentGIF(self):
        self.english.setImage(GIF)
        self.german = makeTranslation(self.english, 'de')
        img_en = self.english.getImage()
        img_de = self.german.getImage()
        self.failUnlessEqual(img_en.content_type, 'image/gif')
        self.failUnlessEqual(img_de.content_type, 'image/gif')

    def testDependent(self):
        self.english.setImageDependent(JPG)
        self.german = makeTranslation(self.english, 'de')
        self.german.setImageDependent(PNG)
        img_en = self.english.getImageDependent()
        img_de = self.german.getImageDependent()
        self.failUnlessEqual(img_en.content_type, 'image/jpeg')
        self.failUnlessEqual(img_de.content_type, 'image/png')
