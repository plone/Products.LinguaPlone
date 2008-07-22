##parameters=
##title=Return deletable languages

lang_names = context.portal_languages.getAvailableLanguages()
translations = context.getNonCanonicalTranslations()

# Return dictionary of information about existing translations
# tuples of lang id, lang name and content title
languages = []
for lang in translations.keys():
    item = translations[lang][0]
    languages.append(dict(id=lang, name=lang_names[lang]['name'],
        title = item.Title().decode('utf8'),
        path = item.absolute_url_path()))
        
def lcmp(x, y):
    return cmp(x['name'], y['name'])

languages.sort(lcmp)
return languages
