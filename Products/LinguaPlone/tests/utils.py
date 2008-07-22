def setupGlobalRequest(request):
    from ZPublisher import Publish
    from thread import get_ident
    Publish._requests[get_ident()] = request

def makeContent(context, portal_type, id='doc', **kw):
    context.invokeFactory(portal_type, id, **kw)
    return getattr(context, id)

def makeTranslation(content, language='en'):
    content.addTranslation(language)
    return content.getTranslation(language)

def sortTuple(t):
    l = list(t)
    l.sort()
    return tuple(l)
