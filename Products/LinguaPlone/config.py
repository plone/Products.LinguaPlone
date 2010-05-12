import os

from Products.Archetypes.Field import ReferenceField

RELATIONSHIP = 'translationOf'

# With translations-aware catalog you only get the results for the current
# language, unless you explicitly ask for all results by providing the
# Language='all' keyword.

I18NAWARE_CATALOG = os.environ.get('PLONE_I18NAWARE_CATALOG', None)
if I18NAWARE_CATALOG is None:
    I18NAWARE_CATALOG = True
else:
    I18NAWARE_CATALOG = I18NAWARE_CATALOG.lower().strip() in ('true', '1')

NOFILTERKEYS = ['Language', 'UID', 'id', 'getId']
I18NAWARE_REFERENCE_FIELDS = [ReferenceField, ]

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
