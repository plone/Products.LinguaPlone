from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import implements
from zope.component import adapts
from types import FunctionType as function

from plone.locking.interfaces import ILockable
from plone.app.layout.navigation.defaultpage import isDefaultPage
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

# Method generation for ITranslatable content with language independent fields
from Products.Archetypes.ClassGen import GeneratorError, _modes
from Products.Archetypes.ClassGen import Generator as ATGenerator
from Products.Archetypes.ClassGen import ClassGenerator as ATClassGenerator
from Products.Archetypes.ArchetypeTool import registerType as registerATType
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.Archetypes.interfaces import IReferenceable

from Products.LinguaPlone.config import KWARGS_TRANSLATION_KEY
from Products.LinguaPlone.config import RELATIONSHIP
from Products.LinguaPlone.config import I18NAWARE_REFERENCE_FIELDS
from Products.LinguaPlone.interfaces import ILanguageIndependentFields
from Products.LinguaPlone.interfaces import ILocateTranslation
from Products.LinguaPlone.interfaces import ITranslatable
from Products.LinguaPlone.interfaces import ITranslationFactory


AT_GENERATE_METHOD = []
_modes.update({
    't' : { 'prefix'   : 'setTranslation',
            'attr'     : 'translation_mutator',
            'security' : 'write_permission',
            },
})

def _translatedOfUID(refcat, source, language):
    """The UID of the translation language of the given source."""
    suid = source
    if isinstance(source, basestring):
        # if we get a uid, lookup the object
        source = refcat.lookupObject(suid)
    elif IReferenceable.providedBy(source):
        suid = source.UID()

    tuid = suid
    if ITranslatable.providedBy(source):
        target = source.getTranslation(language)
        if target:
            tuid = target.UID()
        else:
            canonical = source.getCanonical()
            tuid = canonical.UID()
    return tuid

class Generator(ATGenerator):
    """Generates methods for language independent fields."""

    def makeMethod(self, klass, field, mode, methodName):
        name = field.getName()
        method = None
        if mode == "r":
            def generatedAccessor(self, **kw):
                """Default Accessor."""
                if kw.has_key('schema'):
                    schema = kw['schema']
                else:
                    schema = self.Schema()
                    kw['schema'] = schema
                return schema[name].get(self, **kw)
            method = generatedAccessor
        elif mode == "m":
            def generatedEditAccessor(self, **kw):
                """Default Edit Accessor."""
                if kw.has_key('schema'):
                    schema = kw['schema']
                else:
                    schema = self.Schema()
                    kw['schema'] = schema
                return schema[name].getRaw(self, **kw)
            method = generatedEditAccessor
        elif mode == "w":
            # the generatedMutator doesn't actually mutate, but calls a
            # translation mutator on all translations, including self.
            def generatedMutator(self, value, **kw):
                """LinguaPlone Default Mutator."""
                if kw.has_key('schema'):
                    schema = kw['schema']
                else:
                    schema = self.Schema()
                    kw['schema'] = schema
                # translationMethodName is always present, as it is set in the
                # generator as a method on the mutator method, which is this
                # method :-/
                mutator = getattr(self, schema[name].mutator, None)
                translationMethodName = getattr(mutator, '_lp_mutator', None)
                if translationMethodName is None: # Houston, we have a problem
                    return schema[name].set(self, value, **kw)
                # Instead of additional classgen magic below, we check the
                # languageIndependent property and have a shortcut for the
                # language dependent fields
                if not schema[name].languageIndependent:
                    # Look up the actual mutator and delegate to it.
                    return getattr(self, translationMethodName)(value, **kw)
                # get all translations including self
                translations = [t[0] for t in \
                                hasattr(self, 'getTranslations') and \
                                self.getTranslations().values() or []]
                # reverse to return the result of the canonical mutator
                translations.reverse()
                refcat = getToolByName(self, REFERENCE_CATALOG)
                res = None
                for t in translations:
                    schema = t.Schema()
                    if name not in schema:
                        # don't copy fields not existing in destination schema
                        continue
                    field = schema[name]
                    if type(field) not in I18NAWARE_REFERENCE_FIELDS:
                        # This is a "normal" field:
                        # Look up the actual mutator and delegate to it.
                        res = getattr(t, translationMethodName)(value, **kw)
                        continue
                    # Some kind of reference field:
                    # special handling of at-references start here
                    lang = t.Language()
                    translated_value = None
                    if field.multiValued:
                        if value:
                            if isinstance(value, basestring):
                                value = [value]
                            translated_value = [_translatedOfUID(refcat, u, lang)
                                                for u in value if u]
                    elif value:
                        # single valued and not empty
                        translated_value = _translatedOfUID(refcat, value, lang)
                    translationMethod = getattr(t, translationMethodName)
                    res = translationMethod(translated_value, **kw)
                return res
            # end of "def generatedMutator"
            method = generatedMutator
        elif mode == "t":
            # The translation mutator that changes data
            def generatedTranslationMutator(self, value, **kw):
                """Delegated Mutator."""
                if kw.has_key('schema'):
                    schema = kw['schema']
                else:
                    schema = self.Schema()
                    kw['schema'] = schema
                return schema[name].set(self, value, **kw)
            method = generatedTranslationMutator
        else:
            raise GeneratorError("""Unhandled mode for method creation:
            %s:%s -> %s:%s""" %(klass.__name__,
                                name,
                                methodName,
                                mode))

        # Zope security requires all security protected methods to have a
        # function name. It uses this name to determine which roles are allowed
        # to access the method.
        # This code is renaming the internal name from e.g. generatedAccessor to
        # methodName.
        method = function(method.func_code,
                          method.func_globals,
                          methodName,
                          method.func_defaults,
                          method.func_closure,
                         )
        method._lp_generated = True # Note that we generated this method
        method._lp_generated_by = klass.__name__
        if mode == 'w': # The method to delegate to
            method._lp_mutator = self.computeMethodName(field, 't')
        setattr(klass, methodName, method)


class ClassGenerator(ATClassGenerator):
    """Generates methods for language independent fields."""

    def generateClass(self, klass):
        # We are going to assert a few things about the class here
        # before we start, set meta_type, portal_type based on class
        # name, but only if they are not set yet
        if (not getattr(klass, 'meta_type', None) or
            'meta_type' not in klass.__dict__):
            klass.meta_type = klass.__name__
        if (not getattr(klass, 'portal_type', None) or
            'portal_type' not in klass.__dict__):
            klass.portal_type = klass.__name__
        klass.archetype_name = getattr(klass, 'archetype_name',
                                       self.generateName(klass))

        self.checkSchema(klass)
        fields = klass.schema.fields()
        # Find the languageIndependent fields.
        fields = [field for field in fields if field.languageIndependent]
        self.generateMethods(klass, fields)

    def generateMethods(self, klass, fields):
        generator = Generator()
        for field in fields:
            assert not 'm' in field.mode, 'm is an implicit mode'
            assert not 't' in field.mode, 't is an implicit mode'

            # Make sure we want to muck with the class for this field
            if 'c' not in field.generateMode:
                continue
            typ = getattr(klass, 'type')
            # (r, w)
            for mode in field.mode:
                self.handle_mode(klass, generator, typ, field, mode)
                if mode == 'w':
                    self.handle_mode(klass, generator, typ, field, 'm')
                    self.handle_mode(klass, generator, typ, field, 't')

    def handle_mode(self, klass, generator, typ, field, mode):
        attr = _modes[mode]['attr']
        # Did the field request a specific method name?
        methodName = getattr(field, attr, None)
        if not methodName:
            methodName = generator.computeMethodName(field, mode)

        # If there is already a mutator, make that the translation mutator
        # NB: Use of __dict__ means base class attributes are ignored
        if mode == 'w' and klass.__dict__.has_key(methodName):
            method = getattr(klass, methodName).im_func
            method._lp_renamed = True # Note that we renamed this method
            method._lp_renamed_by = klass.__name__
            setattr(klass, generator.computeMethodName(field, 't'), method)
            delattr(klass, methodName)

        # Avoid name space conflicts
        def want_generated_method(klass, methodName, mode):
            if getattr(klass, methodName, None) is AT_GENERATE_METHOD:
                return True
            if mode == 'r':
                return not hasattr(klass, methodName)
            else: # mode == w|m|t
                return not klass.__dict__.has_key(methodName)

        if want_generated_method(klass, methodName, mode):
            if typ.has_key(methodName):
                raise GeneratorError("There is a conflict"
                                     "between the Field(%s) and the attempt"
                                     "to generate a method of the same name on"
                                     "class %s" % (
                    methodName,
                    klass.__name__))

            # Make a method for this klass/field/mode
            generator.makeMethod(klass, field, mode, methodName)

        # Update security regardless of the method being generated or
        # not. Not protecting the method by the permission defined on
        # the field may leave security open and lead to misleading
        # bugs.
        self.updateSecurity(klass, field, mode, methodName)

        # Note on the class what we did (even if the method existed)
        attr = _modes[mode]['attr']
        setattr(field, attr, methodName)


_cg = ClassGenerator()
generateClass = _cg.generateClass
generateMethods = _cg.generateMethods


def registerType(klass, package=None):
    """Overrides the AT registerType to enable method generation for language
    independent fields"""
    # Generate methods for language independent fields
    generateClass(klass)

    # Pass on to the regular AT registerType
    registerATType(klass, package)


def generateCtor(name, module):
    ctor = """
def add%(name)s(self, id, **kwargs):
    o = %(name)s(id)
    self._setObject(id, o)
    o = self._getOb(id)
    canonical = None
    if kwargs.has_key('%(KWARGS_TRANSLATION_KEY)s'):
        canonical = kwargs.get('%(KWARGS_TRANSLATION_KEY)s')
        del kwargs['%(KWARGS_TRANSLATION_KEY)s']
    o.initializeArchetype(**kwargs)
    if canonical is not None:
        o.addReference(canonical, '%(RELATIONSHIP)s')
    return o.getId()
""" % {'name':name, 'KWARGS_TRANSLATION_KEY':KWARGS_TRANSLATION_KEY,
       'RELATIONSHIP':RELATIONSHIP}

    exec ctor in module.__dict__
    return getattr(module, 'add%s' % name)


# Exact copy of ArchetypeTool.process_type, but with new generateCtor
import sys
from copy import deepcopy
from Products.Archetypes.ArchetypeTool import base_factory_type_information
from Products.Archetypes.ArchetypeTool import modify_fti
def process_types(types, pkg_name):
    content_types = ()
    constructors  = ()
    ftis = ()

    for rti in types:
        typeName = rti['name']
        klass = rti['klass']
        module = rti['module']

        if hasattr(module, 'factory_type_information'):
            fti = module.factory_type_information
        else:
            fti = deepcopy(base_factory_type_information)
            modify_fti(fti, klass, pkg_name)

        # Add a callback to modifty the fti
        if hasattr(module, 'modify_fti'):
            module.modify_fti(fti[0])
        else:
            m = None
            for k in klass.__bases__:
                base_module = sys.modules[k.__module__]
                if hasattr(base_module, 'modify_fti'):
                    m = base_module
                    break
            if m is not None:
                m.modify_fti(fti[0])

        ctor = getattr(module, 'add%s' % typeName, None)
        if ctor is None:
            ctor = generateCtor(typeName, module)

        content_types += (klass,)
        constructors += (ctor,)
        ftis += fti

    return content_types, constructors, ftis

# Language tag splitting
def splitLanguage(tag):
    """Split a language tag (RFC 1766) into components

    Currently, this splits a language tag on the first dash *only*, and will
    not split i- and x- language tags, as these prefixes denote non-standard
    languages.

    """
    try:
        tag = tag.lower()
        if tag[:2] in ('i-', 'x-'):
            return (tag, None)
        tags = tag.split('-', 1)
    except AttributeError:
        # not a string
        tags = []
    tags.extend((None, None))
    return tuple(tags[:2]) # returns (main, sub), (main, None) or (None, None)


def linkTranslations(context, todo):
    """Make content objects in translations of eachother.

    The objects to link are passed in the form an iterable sequence
    of things to connect. The things to connect are specified as a list
    of tuples containing the physical path of the object and the language.
    For example:

      [ [ (["FrontPage"], "en"), (["FrontPage-no"], "no") ],
        [ (["images", "logo"], "en"), (["bilder", "logo"], "no") ] ]

    That will link the FrontPage and FrontPage-no objects together as
    English and Norwegian translation as well as the images/logo and
    bilder/logo objects.
    """

    for task in todo:
        task = [(context.unrestrictedTraverse("/".join(path)), lang)
                    for (path, lang) in task]

        types=set()
        for (object, lang) in task:
            object.setLanguage(lang)
            types.add(object.portal_type)

        if len(types)>1:
            raise ValueError("Not all translations have the same portal type")

        task = [t[0] for t in task]
        if len(task)<=1:
            continue

        (canonical, translations) = (task[0], task[1:])
        for translation in translations:
            translation.addTranslationReference(canonical)
            canonical.setCanonical()


class LocateTranslation(object):
    """Default ILocateTranslation adapter.

    If the parent for an object is translatable and has a translation
    to the desired language that translation will be used as the new
    location. In all other cases the new translation will be put in
    the same location as the current object.
    """
    implements(ILocateTranslation)
    adapts(ITranslatable)

    def __init__(self, context):
        self.context=context


    def findLocationForTranslation(self, language):
        parent = aq_parent(aq_inner(self.context))
        trans_parent = ITranslatable(parent, None)
        if trans_parent is None:
            return parent

        return trans_parent.getTranslation(language) or parent


class TranslationFactory(object):
    """Default translation factory.
    """

    implements(ITranslationFactory)
    adapts(ITranslatable)

    def __init__(self, context):
        self.context=context


    def generateId(self, container, canonical_id, language):
        new_id = canonical_id
        suffix = "-" + str(language)    # unicode breaks `checkValidId()`
        while not container.checkIdAvailable(new_id):
            new_id += suffix

        return new_id


    def getTranslationPortalType(self, container, language):
        return self.context.portal_type


    def createTranslation(self, container, language, *args, **kwargs):
        context = aq_inner(self.context)
        canonical = context.getCanonical()
        portal_type = self.getTranslationPortalType(container, language)
        new_id = kwargs.pop(
            'id', self.generateId(container, canonical.getId(), language))
        kwargs["language"] = language
        translation = _createObjectByType(portal_type, container,
                                          new_id, *args, **kwargs)

        # If there is a custom factory method that doesn't add the
        # translation relationship, make sure it is done now.
        if translation.getCanonical() != canonical:
            translation.addTranslationReference(canonical)

        ILanguageIndependentFields(canonical).copyFields(translation)

        if isDefaultPage(aq_parent(aq_inner(canonical)), canonical):
            translation._lp_default_page=True

        # If this is a folder, move translated subobjects aswell.
        if context.isPrincipiaFolderish:
            moveids = []
            for obj in context.objectValues():
                translator = ITranslatable(obj, None)
                if translator is not None \
                   and translator.getLanguage() == language:
                    lockable = ILockable(obj, None)
                    if lockable is not None and lockable.can_safely_unlock():
                        lockable.unlock()
                    moveids.append(obj.getId())
            if moveids:
                info = context.manage_cutObjects(moveids)
                translation.manage_pasteObjects(info)

        return translation


class LanguageIndependentFields(object):
    """Default language independent fields manager.
    """

    implements(ILanguageIndependentFields)
    adapts(ITranslatable)

    def __init__(self, context):
        self.context = context

    def getFields(self, schema=None):
        if schema is None:
            schema = self.context.Schema()
        return schema.filterFields(languageIndependent=True)

    def getFieldsToCopy(self, translation, source_schema=None,
                        dest_schema=None):
        # Only copy fields that exist in the destination schema.
        if source_schema is None:
            source_schema = self.context.Schema()
        if dest_schema is None:
            dest_schema = translation.Schema()
        fields = self.getFields(source_schema)
        return [x for x in fields if x.getName() in dest_schema]

    def copyField(self, field, translation):
        accessor = field.getEditAccessor(self.context)
        if not accessor:
            accessor = field.getAccessor(self.context)
        if accessor:
            data = accessor()
        else:
            data = field.get(self.context)
        field.getMutator(translation)(data)

    def copyFields(self, translation):
        for field in self.getFieldsToCopy(translation):
            self.copyField(field, translation)
