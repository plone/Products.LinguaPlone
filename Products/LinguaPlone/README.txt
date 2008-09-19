Introduction
============

LinguaPlone aims to be *the* multilingual/translation solution for
Plone, and achieves this by being as transparent as possible and by
minimizing the impact for existing applications and Plone itself.

It utilizes Archetypes references to do the translation, and all content
is left intact both on install and uninstall - thus, it will not disrupt
your content structure in any way. It also works with WebDAV and FTP.

LinguaPlone doesn't require a particular hierarchy of content, and will
work with any layout of your content space.

Some benefits of LinguaPlone
----------------------------

- Totally transparent, install-and-go.

- Each translation is a discrete object, and can be workflowed
  individually.

- This also means that it works with WebDAV and FTP.

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

- Uses the notion of Canonical versions, so you can do interesting things
  with workflow, like invalidate all translations of a document when the
  master copy has changed.


Dependencies
============

Requires the following minimum versions:

- Plone 3.1.5


Installation
============

If you are upgrading LinguaPlone there may be an upgrade step that you
need to do.  Please check the manage_upgrades tab in portal_setup (in
the Zope Management Interface or ZMI).  First do this, then do a
reinstall in the ''Add-on Products' control panel.


Frequently asked questions
==========================

I see no language flags and switching language does not work
------------------------------------------------------------

This happens if the cookie language negotiation scheme is not enabled. Look
at the ``portal_languages`` tool in the ZMI and check if ``Use cookie for
manual override`` is enabled.


LinguaPlone - quick demo instructions
=====================================

LinguaPlone ships with a few example types that demonstrates the translation
mechanism. It's trivial to add this to your own classes (see the README),
but to save you the hassle, you can try this simple experiment:

- Make sure you have Plone 3.1.5 or newer installed.

- Put LinguaPlone in your Products directory

- (Re)start Zope

- 'Site Setup' &rarr; 'Add/Remove Products', install LinguaPlone

For the demonstration to make sense, we need to define a list of languages:

- Go to the Site Setup

- Click 'Language Settings'

- Select 3-4 languages from the selection list. Note that the languages are
  listed in their native name, so the sorting might be a bit unexpected
  (Spanish is Espanol, for example)

- Press 'Save'

Now we have a few languages to play with, and can go back to the Plone
interface. Notice how you now have flags indicating your selected languages
under the print/sendto area.

We now want to add a simple type:

- Add a 'Page'.

- After filling out the type with some content and clicking 'Save', you will
  see that this content type has a pulldown menu, 'Translate into'.

- Select a language you want to translate this document into.

- Save this translation.

- Try to switch languages by clicking the flags.

That's a very simple use case for the multilingual types.


Developer Usage
===============

You can test it by multilingual-enabling your existing AT content types
(see instructions below),  or by testing the simple included types.
Don't forget to select what languages should be available in
'portal_languages' in the ZMI. :)


Credits
=======

LinguaPlone was donated to the Plone Foundation by Jarn AS in March 2006.

Design and development --
  Jarn_ (Alexander Limi, Dorneles Tremea, Geir Baekholt, Helge Tesdal, Stefan H. Holek, Wichert Akkerman)

Original design idea:
  `Object realms`_ (Benjamin Saller, Kapil Thangavelu)

Funding and deployment, initial version:
  Oxfam International

.. _Jarn: http://www.jarn.com
.. _Object realms: http://www.objectrealms.net/

Additional funding/sponsorship:
  Hitotsubashi University in Tokyo, Centre for New European studies
  (Jonathan Lewis)

Funding Plone 2.0.x compatibility:
  Zope Japan Corporation
  (Takeshi Yamamoto)

Also many thanks to

Simon Eisenmann:
   For doing the hard job of the first implementations (I18NLayer)
   we had to learn from before doing this.

Learning Lab Denmark:
   For contributing and sponsoring the experience needed to build a
   multilingual solution.

Nate Aune:
   For always pushing for the better solution and making us realise
   LinguaPlone had to be built.

Jodok Batlogg:
   For extensive testing, deploying and feedback.

Sasha Vincic:
   For testing and expanding and making cool new stuff happen with
   LinguaPlone, XLIFF import/export in particular.


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
(like start and end on Events) are referenced directly.

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
      from Products.LinguaPlone.atapi import *
  except ImportError:
      # No multilingual support
      from Products.Archetypes.public import *

For the fields that are language independent, you add
'languageIndependent=True' in the schema definition.

License
=======

  GNU General Public License, version 2.1
