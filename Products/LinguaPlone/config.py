from zLOG import LOG, INFO

GLOBALS = globals()
PKG_NAME = "LinguaPlone"
SKIN_NAME = "LinguaPlone"

SKIN_LAYERS = (SKIN_NAME,)

RELATIONSHIP = 'translationOf'

INSTALL_DEMO_TYPES = 0 ##Install the demo types
DEBUG = 0  ## See debug messages

# If true the global request patch should be applied.
GLOBAL_REQUEST_PATCH = 1

# I18N-aware reference tool will look up the correct translation when you look
# up a reference, unless you ask the tool not to.
# Only use if you understand the implications.
I18NAWARE_REFERENCE_TOOL = 0

# With cache translations, getCanonical() and getTranslations() will be cached.
# However, it might lead to read inconsistencies between threads and ZEO clients
CACHE_TRANSLATIONS = 0

# With translations-aware catalog you only get the results for the current
# language, unless you explicitly ask for all results by providing the
# Language='all' keyword.
I18NAWARE_CATALOG = 1
NOFILTERKEYS = ['Language', 'UID', 'id', 'getId']

# When auto-notification is enabled, editing the canonical translation object
# will automatically invalidate all translations.
# With this off you must manually invalidate translations by calling their
# notifyCanonicalUpdate() method or through the invalidateTranslations() API.
AUTO_NOTIFY_CANONICAL_UPDATE = 1

# With delete protection on, the canonical translation object can
# only be deleted if there are no more translations left.
# In other words: You have to delete all translations before you can
# delete the canonical translation object.
CANONICAL_DELETE_PROTECTION = 0

# This key is used by the constructor when creating translations
# to make sure translation linking is done within the invokeFactory and
# before notifyWorkflowCreated.
KWARGS_TRANSLATION_KEY = 'linguaplone_languageOf'

def log(msg, level=INFO):
    LOG(PKG_NAME, level, msg)
