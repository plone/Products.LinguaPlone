.. image:: https://api.travis-ci.org/jfroche/Products.LinguaPlone.png
   :target: http://travis-ci.org/jfroche/Products.LinguaPlone

Introduction
============

LinguaPlone is *the* multilingual/translation solution for Plone, and achieves
this by being as transparent as possible and by minimizing the impact for
existing applications and Plone itself.

It utilizes the Archetypes reference engine to do the translation, and all
content is left intact both on install and uninstall - thus, it will not
disrupt your content structure in any way.

LinguaPlone doesn't require a particular hierarchy of content, and will in
theory work with any layout of your content space, though the default layout
advertised in the install instructions will make the site easier to use.

Some benefits of LinguaPlone
----------------------------

- Totally transparent, install-and-go.

- Each translation is a discrete object, and can be workflowed individually.

- Translations are kept track of using AT references.

- You can multilingual-enable your types without affecting their operation
  outside LinguaPlone.

- Even if you uninstall LinguaPlone after adding multilingual content, all
  your content will be intact and will work as separate objects! The only
  thing that will be inactive is the references between the objects. If you
  re-install it, they will be back. It's very non-intrusive.

- Supporting multilingual capabilities is a 4 (!) line addition to your
  Archetypes class, and does not alter the functionality of the class when
  used outside LinguaPlone.

- Fully integrated with ATContentTypes, so the basic content types are
  translatable.

- Supports language-independent fields (example: dates, first/last names)
  for fields you want to be the same across translations, and updated in all
  languages if one of them changes.

- Uses the notion of canonical versions, so you can do interesting things
  with workflow, like invalidate all translations of a document when the
  master copy has changed.


Installation
============

Install LinguaPlone into your Plone environment by adding it to the buildout or
adding it as a dependency of your policy package and rerun buildout.

Next add a new Plone site and select the `LinguaPlone` add-on. Make sure to
specify the primary language of your site. Continue to the language control
panel and specify all other languages you want to support.

Prepare the content structure by calling `@@language-setup-folders` on your
Plone site root, for example::

  http://localhost:8080/Plone/@@language-setup-folders

You might want to clean up the default content or move it around by visiting::

  http://localhost:8080/Plone/folder_contents

and deleting the Events, News and Users folders.

After following all these steps you have a good starting point to build a
multilingual site. Whether or not you have the same site structure in each
of the language folders is up to you and your requirements. By using the top
level language folders every URL corresponds to exactly one language which is
good for search bots and makes caching a lot easier. It also means that you
don't have folders with mixed languages in them, which improves the usability
for editors a lot, since they don't have to worry about switching languages in
the same folder just to see if there's more content in them.

The Plone site root is the only exception here and setup with a language
switcher default view that does the language negotiation and redirects users
to the right URL.


Upgrade
=======

If you are upgrading LinguaPlone there may be an upgrade step that you need to
do. Please check the 'Add-ons' control panel for this.


Uninstallation
==============

If you no longer want to use LinguaPlone, you can remove it from your site.

First you need to deactivate LinguaPlone in the add-ons control panel. After
you did this you can remove LinguaPlone from your Plone environment on the file
system. If you forget to do the deactivation step, add LinguaPlone back
temporarily and deactivate it properly. Otherwise you'll likely not be able to
use their site with errors relating to the `SyncedLanguages` utility.


Frequently asked questions
==========================

I see no language flags and switching language does not work
------------------------------------------------------------

This happens if the cookie language negotiation scheme is not enabled. Look
at the ``portal_languages`` tool in the ZMI and check if ``Use cookie for
manual override`` is enabled.

If the language selection links point to URL's containing `switchLanguage` the
wrong language selector from core Plone is active. Go to the control panel and
check if you can select multiple languages on the language control panel. If
you cannot, LinguaPlone isn't properly installed.

If you can select multiple languages only the language selector viewlet is
wrong. Make sure you haven't customized the viewlet and put it into a different
viewlet manager. The viewlet is only registered for the
`plone.app.layout.viewlets.interfaces.IPortalHeader` manager. You need to
register the languageselector viewlet from `LinguaPlone/browser/configure.zcml`
for your new viewlet manager as well.


Developer Usage
===============

You can test it by multilingual-enabling your existing AT content types (see
instructions below), or by testing the simple included types. Don't forget to
select what languages should be available in the language control panel.


Implementation details
======================

Architecture
------------

LinguaPlone can only be used with Archetypes based content types.
It provides a I18NBaseObject class that implements a ITranslatable interface
that handles the translation linking. LinguaPlone provides base classes that
inherits from I18NBaseObject and the regular AT base classes.

Language independent fields
---------------------------

Language independent fields are looked up from the canonical (original)
translation.

The value is also stored on each translated object so every object has every
attribute in case it is moved out of a translation context or some attributes
(like start and end on events) are referenced directly.

Language independence is set in the AT schema definition. Only AT based
content types can have language independent fields.

Language lookup
---------------

The language tool returns a list of languages to look for. If there is no
fallback, there will be only one element in the list.


Enable multilingual support in your content types
-------------------------------------------------

At the top, **instead** of ``from Products.Archetypes.atapi import *``, you
add::

  try:
      from Products.LinguaPlone import atapi
  except ImportError:
      # No multilingual support
      from Products.Archetypes import atapi

For the fields that are language independent, you add
``languageIndependent=True`` in the Archetypes schema definition.

Example::

    atapi.StringField(
        'myField',
        widget=atapi.StringWidget(
        ....
        ),
        languageIndependent=True
    ),

Language independent fields are correctly shared between linked translations only if 
your content type uses LinguaPlone imports as described above.

For more LinguaPlone related programming examples see 
`Translating content <http://collective-docs.readthedocs.org/en/latest/i18n/translating_content.html>`_
in Plone Developer Documentation.


Developer information
=====================

* Home page: http://plone.org/products/linguaplone
* Issue tracker: http://plone.org/products/linguaplone/issues
* Code repository: https://svn.plone.org/svn/plone/Products.LinguaPlone/trunk
* Mailing list: https://lists.sourceforge.net/lists/listinfo/plone-i18n


License
=======

GNU General Public License, version 2
