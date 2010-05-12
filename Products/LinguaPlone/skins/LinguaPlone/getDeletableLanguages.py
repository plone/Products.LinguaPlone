##parameters=
##title=Return deletable languages

from Products.CMFPlone.utils import safe_unicode

lang_names = context.portal_languages.getAvailableLanguages()
translations = context.getTranslations(
    include_canonical=False, review_state=False)

# Return dictionary of information about existing translations
# tuples of lang id, lang name and content title
languages = []
for lang, item in translations.items():
    languages.append(dict(id=lang, name=lang_names[lang]['name'],
        title = safe_unicode(item.Title()),
        path = item.absolute_url_path()))

def lcmp(x, y):
    return cmp(x['name'], y['name'])

languages.sort(lcmp)
return languages
