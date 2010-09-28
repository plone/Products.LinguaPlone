Overview
========

This sub-package provides a framework for syncing criteria as known from
ATContentTypes collections (Topic's) across language versions. This is similar
in scope as language independent fields for normal Archetypes objects.

Caveats
-------

There is currently no user interface exposure of this framework. The
functionality is also not invoked automatically, but currently left to manual
calling from an application specific UI.

In order to work, all criteria types currently need to be addable to the Topic
type, by adding them all to the ``allowed_content_types`` list on the Topic
FTI.

The framework uses a specific ``syncer`` adapter per criteria type, so it only
handles criteria defined in ATContentTypes. You will need to add your own
adapter for custom criteria types.

The framework allows to use custom behavior for a specific index name and
criteria type combination. This is implemented by first looking up a named
adapter for the index name and falling back to the general adapter. This allows
to handle string criteria for the ``review_state`` in a language independent
manner (review states are technical ids) while generally all strings criteria
are language dependent. If you have custom indexes you might need to review
them and adjust their behavior. The named adapter registration serves as the
equivalent to the ``languageIndependent`` marker set on fields.

The code was written for a project which had a consistent site hierarchy
across all languages and where all translations to all languages existed in
all cases. While the code should not assume such a setup and care has been
taken to be defensive in the assumptions, there's likely edge-cases that aren't
covered yet.

Use
---

In its most simple form this can be called by invoking the following code on
a canonical collection:

  >>> from zope.component import queryAdapter
  >>> from Products.LinguaPlone.criteria.interfaces import ICollectionSyncer

  >>> syncer = queryAdapter(collection, ICollectionSyncer)
  >>> if syncer is not None:
  >>>     syncer.sync()


Afterwards all translations should have the same criteria and their values
should match the canonical or be adjusted to match the translation. For example
reference criteria will use a target reference in the translations language.
