from plone.i18n.locales.interfaces import ILanguageAvailability
from zope.component import getGlobalSiteManager
from zope.i18nmessageid import Message, MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.CMFCore.utils import getToolByName

_ = MessageFactory('linguaplone')


def sort_key(language):
    return language[1]


@implementer(IVocabularyFactory)
class AllContentLanguageVocabulary(object):
    """Vocabulary factory for all content languages in the portal.
    """

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ltool = getToolByName(context, 'portal_languages')
        gsm = getGlobalSiteManager()
        util = gsm.queryUtility(ILanguageAvailability)
        if ltool.use_combined_language_codes:
            languages = util.getLanguages(combined=True)
        else:
            languages = util.getLanguages()

        items = [(l, languages[l].get('name', l)) for l in languages]
        items.sort(key=sort_key)
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

AllContentLanguageVocabularyFactory = AllContentLanguageVocabulary()


@implementer(IVocabularyFactory)
class UntranslatedLanguagesVocabulary(object):
    """Vocabulary factory returning untranslated languages for the context.
    """

    def __init__(self, incl_neutral=False, incl_nochange=False):
        self.incl_neutral = incl_neutral
        self.incl_nochange = incl_nochange

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ltool = getToolByName(context, 'portal_languages')
        supported = dict(ltool.listSupportedLanguages())
        translated = context.getTranslationLanguages()

        # List all languages not already translated
        languages = [lang for lang in supported if lang not in translated]

        items = [(l, supported[l]) for l in languages]
        items.sort(key=sort_key)
        items = [SimpleTerm(i[0], i[0], i[1].decode('utf-8')) for i in items]
        if self.incl_neutral:
            neutral = SimpleTerm(
                "neutral",
                "neutral",
                _("label_neutral", default=u"Neutral"),
            )
            items.insert(0, neutral)
        if self.incl_nochange:
            nochange = SimpleTerm(
                "nochange",
                "nochange",
                Message(
                    "label_no_change",
                    domain="plone",
                    default=u"No change",
                ),
            )
            items.insert(0, nochange)
        return SimpleVocabulary(items)

UntranslatedLanguagesVocabularyFactory = UntranslatedLanguagesVocabulary()
NeutralAndUntranslatedLanguagesVocabularyFactory = \
    UntranslatedLanguagesVocabulary(incl_neutral=True)
NoChangeNeutralAndUntranslatedLanguagesVocabularyFactory = \
    UntranslatedLanguagesVocabulary(incl_neutral=True, incl_nochange=True)


@implementer(IVocabularyFactory)
class DeletableLanguagesVocabulary(object):
    """Vocabulary factory returning deletable languages for the context.
    """

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ltool = getToolByName(context, 'portal_languages')
        available = ltool.getAvailableLanguages()
        translations = context.getTranslations(
            include_canonical=False, review_state=False)

        items = []
        for lang, item in translations.items():
            info = available[lang]
            desc = u"%s (%s): %s" % (
                info.get(u'native', info.get(u'name')),
                lang,
                item.Title().decode('utf-8'),
            )
            items.append(SimpleTerm(lang, lang, desc))

        return SimpleVocabulary(items)

DeletableLanguagesVocabularyFactory = DeletableLanguagesVocabulary()
