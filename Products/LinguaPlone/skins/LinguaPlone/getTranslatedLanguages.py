##parameters=
##title=Return translated languages

allLanguages = context.portal_languages.listSupportedLanguages()
translated = context.getTranslationLanguages()

# Only return available translations if they are in the allowed langs from languageTool
languages = [lang for lang in allLanguages if lang[0] in translated]

def lcmp(x, y):
    return cmp(x[1], y[1])

languages.sort(lcmp)
return languages
