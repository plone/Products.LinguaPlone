from Products.CMFCore.utils import ContentInit
from Products.LinguaPlone.public import *
from Products.LinguaPlone import config
from Products.LinguaPlone import permissions

from zope.i18nmessageid import MessageFactory
LinguaPloneMessageFactory = MessageFactory('linguaplone')

def checkVersion():
    from Products.CMFPlone.utils import getFSVersionTuple
    if getFSVersionTuple()[:3] < (3,0,1):
        import logging, sys
        logger=logging.getLogger("LinguaPlone")
        logger.log(logging.ERROR,
                "Unsupported Plone version: " 
                "LinguaPlone 2.0 requires Plone 3.0.1 or later")
        sys.exit(1)

checkVersion()

def initialize(context):
    # Apply monkey patches
    from Products.LinguaPlone import patches

    if config.INSTALL_DEMO_TYPES:
        import examples

    # Initialize content types
    content_types, constructors, ftis = process_types(
        listTypes(config.PKG_NAME), config.PKG_NAME)

    ContentInit(
        '%s Content' % config.PKG_NAME,
        content_types = content_types,
        permission = permissions.AddPortalContent,
        extra_constructors = constructors,
        fti = ftis,
    ).initialize(context)
    
    from Products.LinguaPlone import LanguageIndex
    context.registerClass(
        LanguageIndex.LanguageIndex, 
        permission=permissions.AddLanguageIndex,
        constructors=(LanguageIndex.manage_addLanguageIndexForm,
                      LanguageIndex.manage_addLanguageIndex),
        icon='www/index.png',
        visibility=None)
