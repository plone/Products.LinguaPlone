def makeContent(context, portal_type, id='doc', **kw):
    context.invokeFactory(portal_type, id, **kw)
    return getattr(context, id)


def makeTranslation(content, language='en'):
    content.addTranslation(language)
    return content.getTranslation(language)
