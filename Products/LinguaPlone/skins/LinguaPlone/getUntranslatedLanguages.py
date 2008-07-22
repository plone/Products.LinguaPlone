##parameters=
##title=Return untranslated languages

allLanguages = context.portal_languages.listSupportedLanguages()
translated = context.getTranslationLanguages()

# List all languages not already translated
languages = [lang for lang in allLanguages if lang[0] not in translated]

def lcmp(x, y):
    return cmp(x[1], y[1])

languages.sort(lcmp)
return languages
