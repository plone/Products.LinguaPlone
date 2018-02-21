Changelog
=========

4.2.2 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- The breadcrumb shown on the translation linker pop-up shows the full site
  [erral]

- Translation linker pop-up is opened on the portal root
  [erral]

Bug fixes:

- *add item here*


4.2.1 (2017-04-03)
------------------

Bug fixes:

- Fix translation menu for combined language codes [fRiSi]


4.2 (2017-03-09)
----------------

New features:

- Show the native language name on the "Translate into..." menu
  [erral]

Bug fixes:

- Fix import location for Products.ATContentTypes.interfaces.
  [thet]

- Don't fail while uninstalling, if LinguaPlone is already uninstalled.
  [thet]


4.1.8 (2017-01-12)
------------------

Bug fixes:

- Fix Home link in the translationbrowser_popup template to point to
  navigation root, not the site root.
  [vincentfretin]

- Add tests for sitemap
  [djowett]


4.1.7 (2016-11-10)
------------------

Bug fixes:

- Fixed bug where even Manager could not view a folder with private default page.
  Fixes https://github.com/plone/Products.CMFPlone/issues/1822
  [maurits]

- Fixed CSRF protection bug on @@language-setup-folders view.
  [syzn]


4.1.6 (2016-11-09)
------------------

Bug fixes:

- Show also current language link in header hreflang links.
  [erral]


4.1.5 (2016-08-11)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


4.1.4 (2016-02-17)
------------------

- Language selector: add form variables
  only when method is GET
  [gotcha]

- Fix handling of deleted or renamed "default page" items.
  [witsch]

- Add uninstall profile.
  [thet]

- Fixed permission for manage_translations_form, anonymous can't access the page
  anymore.
  [prospchr]

- getTypeInfo : defer computation of isCanonical
  [gotcha]

- Fix tests
  [jfroche]

- Set default field value if nothing is given in mutator value
  [jfroche]

- Add Travis buildout
  [jfroche]


4.1.3 (2013-01-18)
------------------

- Fix regression from the plone site root change. When accessing the zope
  root using the ZMI getSite returns empty, so fall back to traversing.
  [pjstevns]

- Add a better way in getting plone site root. A change in Archetypes setting
  the creation date by a subscriber breaks the old way, because traversing
  wasn't avaliable in such an early state.
  [hoka]

- Add a viewlet to mark the translated content as suggested by Google at
  http://googlewebmastercentral.blogspot.com.es/2011/12/new-markup-for-multilingual-content.html
  [erral]

- Update bootstrap.py for zc.buildout 1.5.0.
  [pjstevns]

- Deal with broken translations, esp. when the content's language doesn't
  match the parent's language.
  [pjstevns]

- Fixed getting deletable languages if a language has been disabled and content
  has been translated in this language.
  [kroman0]

- Added option to disable left portlets in translation view.
  [pingviini]

- Fixed translation view to actually hide portlets when configured to do so.
  [pingviini]

- Display the translation of the folder default page in the current language
  if available.
  [pjstevns]

- Check if the forward transition exists before taking it
  [giacomos]

- Fixed preview of "renderable" fields that are not simply text/html (like
  text/x-rst).
  [keul]

- Adjust behavior to current BaseObject by using check_auto_id=True in
  processFormto not force rename_after_creation. This fix
  plone.api.content.create use when you have linguaPlone and you dont set id
  [toutpt]

4.1.2 (2012-02-07)
------------------

- Translation helper scripts (getTransaltedLanguages, getUntranslatedLanguages,
  getDeletableLanguages) are now view methods.
  [thomasdesvenain]

- Display the translation of the folder default page in the current language
  when the folder is neutral.
  [thomasdesvenain]

- Avoid problems when setLanguage is given a null value that is not ''.
  [thomasdesvenain]


4.1.1 (2011-11-15)
------------------

- New translations still had no proper id.
  fix http://plone.org/products/linguaplone/issues/246
  [gotcha]


4.1 (2011-11-14)
----------------

- New translations did not get a proper id.
  fix http://plone.org/products/linguaplone/issues/246
  [jfroche]

- Check 'Add portal content' permission on parent to display translate menu items.
  Check 'Delete objects' on parent or 'Modify portal content' on content
  to display "Manage translations" menu itme.
  Check user has one of those permissions to display menu.
  Refs http://dev.plone.org/plone/ticket/12223.
  [thomasdesvenain]

- Update to require Plone 4.1.
  [hannosch]

- Notify p.a.caching to purge translations when the canonical object is purged.
  [ggozad, stefan]

- Changed permission for the controlpanel to `plone.app.controlpanel.Language`.
  This allows users with the `Site Administrator` role to access it.
  [toutpt]

4.0.4 - 2011-07-25
------------------

- Selector should not propose link to inaccessible content (content for which
  the user does not have View permission). If a translation exist but is
  inaccessible, follow the acquisition chain until a translated item is
  accessible. In case we get to an inaccessible INavigationRoot, do not show
  the language at all.
  [gotcha]

- Removed broken icons and fix invalid XHTML in translation browser popup.
  [hannosch]

- Link to translation browser popup was broken in some VirtualHost setups.
  This closes http://plone.org/products/linguaplone/issues/277.
  [tgraf, hannosch]

- Use template parameter in language selector's viewlet zcml declaration. This
  makes it easier to customize in add-ons. The change requires plone.app.i18n
  2.0.1 or greater.
  [toutpt]

- Force translate menu flag icons dimensions to 14x11 px, so that it's
  consistent with language selector menu. Works with
  plone.app.contentmenu 2.0.4+.
  [thomasdesvenain]

- Changed policy for preserving the view/template in the language selector. We
  only do this if the target item is a direct translation of the current
  context. Otherwise we might link to views which are not available on the
  target content type.
  [thomasdesvenain, hannosch]

- translate_item form works when content has no 'default' fieldset.
  [thomasdesvenain]

- Declare plone.app.iterate dependency.
  [thomasdesvenain]

4.0.3 - 2011-05-27
------------------

- Changed string exceptions to ValueErrors in `translate_edit.cpy`.
  [robert]

- Fix the tests to work with GenericSetup 1.6.3+.
  [hannosch]

- Explicitly load the CMF permissions before using them in a `configure.zcml`.
  [hannosch]

4.0.2 - 2011-01-26
------------------

- Force the user to select a language before attempting to translate
  neutral content items. One content item can be either neutral or have
  translations, but not a mix of the two.
  [witsch]

- Don't create an extra folder when translating the default page of a
  language-neutral folder.
  [witsch]

4.0.1 - 2011-01-10
------------------

- Changed defaultLanguage behavior in I18NBaseObject to always report the
  parent's folder language even if it is neutral.
  [ggozad]

4.0 - 2010-11-25
----------------

- Fixed possible XSS security issue in the `translationbrowser_popup` caused
  by displaying unfiltered content from the `Description` string field as HTML.
  Issue reported by Andrew Nicholson.
  [hannosch]

- Protect against accidentally acquiring the `getTranslations` method from a
  parent object in `utils.generatedMutator`. Thanks to Matous Hora for the
  patch. This closes http://plone.org/products/linguaplone/issues/257.
  [hannosch]

4.0b1 - 2010-11-04
------------------

- Gracefully deal with multiple brains per `UID` in `translated_references`.
  [hannosch]

4.0a4 - 2010-10-06
------------------

- Avoid module global imports in our top-level ``__init__``. If you have
  accidentally imported any of the contents of the ``public`` module directly
  from ``Products.LinguaPlone``, you will need to adjust those to import from
  the ``public`` module instead. This closes
  http://plone.org/products/linguaplone/issues/253.
  [hannosch, ggozad, shh42]

4.0a3 - 2010-09-24
------------------

- Rewrote ``getTranslationReferences`` and ``getTranslationBackReferences``
  internals to avoid the catalog search API and make use of knowledge of its
  internals.
  [hannosch]

- In the TranslatableLanguageSelector only append a question mark, if there's
  a query string to append.
  [hannosch]

4.0a2 - 2010-09-08
------------------

- Make the ``set_language`` query string addition configurable via a class
  variable on the TranslatableLanguageSelector.
  [hannosch]

4.0a1 - 2010-07-28
------------------

- Added test for deleting canonical folders. Added minimum version requirement
  on Products.ATContentTypes 2.0.2 for the fix to
  http://plone.org/products/linguaplone/issues/241.
  [hannosch]

- Fixed language selector logic to correctly deal with all kinds of VHM rules.
  This closes http://plone.org/products/linguaplone/issues/240.
  [hannosch]

- Change the language selector viewlet to be shown in the IPortalHeader manager
  to be consistent with the new default location in Plone 4. This closes
  http://plone.org/products/linguaplone/issues/248.
  [hannosch]

- Require at least Zope 2.12.5 and remove the `-C` work around.
  [hannosch]

- Renamed migrations module to upgrades to match current nomenclature.
  [hannosch]

- Removed Archetypes uid and reference catalog GenericSetup handlers. These
  are part of Archetypes now.
  [hannosch]

- Removed Plone 3.3 specific tests.
  [hannosch]

- Added tests for all upgrade steps.
  [hannosch]

- Removed all dependencies on zope.app packages.
  [hannosch]

- Specify all package dependencies.
  [hannosch]

- Added dependency on Plone 4. Please use a release from the 3.x series if
  you are using Plone 3.
  [hannosch]

3.1 - 2010-07-28
----------------

- No changes.

3.1b1 - 2010-07-18
------------------

- Update license to GPL version 2 only.
  [hannosch]

- If catalog filter attributes contain "Language", and "Language" is
  set to all, don't add Language filters to the REQUEST object
  [do3cc]

3.1a5 - 2010-06-22
------------------

- Use a normal FieldIndex in the uid_catalog and correct custom setuphandler
  to create a functional FieldIndex.
  [hannosch]

3.1a4 - 2010-06-18
------------------

- Removed example types, Plone's default types are LinguaPlone aware and
  provide a good demo of the functionality.
  [hannosch]

- Refactored tests and conform to PEP8 in more places.
  [hannosch]

- Changed the default index used for Language to be a normal FieldIndex. For
  most sites this is sufficient and avoids the major performance hit the
  LanguageIndex brings with it.
  [hannosch]

- Refactor selector code to make it easier to write unit tests for it.
  [hannosch]

- Added development information to README, this closes
  http://plone.org/products/linguaplone/issues/242.
  [hannosch]

- Lessen optimization in selector code, to deal with folderish objects used as
  default pages, refs http://plone.org/products/linguaplone/issues/228.
  [hannosch]

- Removed iterator for tabindex for Plone 4 compatibility.
  [hpeteragitator]

3.1a3 - 2010-05-25
------------------

- Small optimizations in invalidateTranslations, deletable language vocabulary
  and script - avoiding review state calculation and full object lookups.
  [hannosch]

- Removed logger instance and log method from ``config.py``.
  [hannosch]

- Removed unused variables from ``config.py``: ``DEBUG``, ``GLOBALS``,
  ``PKG_NAME``, ``SKIN_LAYERS``, ``SKIN_NAME``, ``INSTALL_DEMO_TYPES``.
  [hannosch]

- Added a general collection criteria translation sync functionality including
  language independent criteria support. This is currently not activated
  automatically and has no UI support yet. See the ``README.txt`` in the
  criteria sub-package for more caveats.
  [hannosch]

- Added tests to prove that indexing and updating reference fields works.
  [hannosch]

- Also handle multiValued references given by a tuple instead of a list in
  ``utils.translated_references``.
  [thet]

- Mini-optimization in language selector.
  [hannosch]

3.1a2 - 2010-03-29
------------------

- Fixed isCanonical inside portal_factory which could lead to strange errors.
  Thanks to Daniel Kraft for the patch. This closes
  http://plone.org/products/linguaplone/issues/236, 237 and 239.
  [hannosch]

- Links in the language selector where broken when using ``_vh_`` parts.
  This closes http://plone.org/products/linguaplone/issues/235.
  [ramon]

- Expanded test coverage extensively. Going from 84% to 93%.
  [hannosch]

- Removed unfinished ``new_manage_translations_form`` prototype.
  [hannosch]

- Silence the ``manage_*`` warnings for the example and test types.
  [hannosch]

- Convert GenericSetup steps registrations to ZCML.
  [hannosch]

- Removed all BBB imports for InitializeClass. We depend on Plone 3.3 which
  comes with Zope 2 versions with the forward compatible import locations, as
  introduced in Zope 2.10.8.
  [hannosch]

- Removed old type actions from example and test types.
  [hannosch]

- Some PEP8 cleanup and minor documentation updates.
  [hannosch]

3.1a1 - 2010-02-19
------------------

- Factor out filtering of "Language" parameter so it can be reused elsewhere.
  [hannosch, witsch]

- Made the manage_translations_form compatible with Plone 4 by replacing a
  call to referencebrowser_startupDirectory with hardcoding the current context
  as the startup directory.
  [huub_bouma]

- Added workflow transitions to the setup view to publish the language folders.
  [hannosch]

- Changed the setup view to give the folders native language titles.
  [hannosch]

- Added automatic setup of the language switcher to the setup view.
  [hannosch]

- Added new ``language-switcher`` view usable as a default view method for the
  Plone site object to dispatch to the appropriate language root folder.
  [hannosch]

- Added new ``language-setup-folders`` helper view to set up a regular structure
  of language root folders for each supported language each marked as a
  navigation root.
  [hannosch]

- Added more CSS classes to the language selector making it possible to target
  each language. Inspired by http://www.thirtysomething.it/.
  [hannosch]

- Only register the catalog export import handlers if they aren't already part
  of Archetypes. This avoids conflicts in Plone 4.0.
  [hannosch]

3.0.1 - 2010-02-02
------------------

- Adjusted the FAQ related to changing the language of an item. This closes
  http://plone.org/products/linguaplone/issues/234.
  [hannosch]

- Clarify ITranslatable interface description for the getTranslation method.
  This closes http://plone.org/products/linguaplone/issues/226.
  [hannosch]

- Made language index more forgiving when dealing with broken canonical
  references. This closes http://plone.org/products/linguaplone/issues/231.
  [hannosch]

- Fixed a regression introduced in 3.0b4. The title of translations wasn't
  generated from the title anymore. While we retain the ability to specify an
  explicit id, by default the new id is now generated from the title again.
  This closes http://plone.org/products/linguaplone/issues/233.
  [hannosch]

- The language portlet was broken due to a prior change of the selector.
  [jensens]

- Small documentation updates.
  [hannosch]

3.0 - 2009-12-21
----------------

- No changes from last release candidate.
  [hannosch]

3.0c4 - 2009-12-07
------------------

- Made it possible to disable the i18n aware catalog feature via an environment
  variable called ``PLONE_I18NAWARE_CATALOG``.
  [hannosch]

3.0c3 - 2009-11-25
------------------

- Made the translated reference functionality more resilient against errors.
  We overwrote the target ``value`` inside the loop setting the references on
  translations. In case of an invalid target in one language, this caused all
  subsequent translations to fail with a different error.
  [hannosch]

3.0c2 - 2009-11-16
------------------

- Silence reference exceptions raised inside the reference multiplexing.
  A normal user cannot do anything about them, so we log them instead.
  [hannosch]

- Changed import from deprecated Products.Archetypes.public to
  Products.Archetypes.atapi.
  [maurits]

- Explicitly define ``portal`` inside the style_slot.
  [maurits]

- Replaced the css_slot with the style_slot, as it is deprecated.
  [maurits]

- Use new shared plonetest config file.
  [hannosch]

3.0c1 - 2009-11-04
------------------

- Don't fail on broken references in ``translated_references``.
  [hannosch]

- Adjusted tests to new default page behavior in Plone 4.
  [hannosch]

- Made use of the new getTranslations API and avoid calculating the review
  state if it is not required.
  [hannosch]

- Fixed functional tests to avoid an extraneous slash in the URL.
  [hannosch]

- Added a new I18NOnlyBaseBTreeFolder mix-in, which can be used in Plone 4 to
  give LinguaPlone behavior to the new plone.app.folder types.
  [hannosch]

- Avoid deprecation warnings for the use of the Globals package.
  [hannosch]

3.0b8 - 2009-10-22
------------------

- Adjusted the language selector to point to the nearest translation for each
  language. So far the selector only worked on items which had translations
  into all languages. Otherwise the content language negotiator would render
  the selector useless. This closes
  http://plone.org/products/linguaplone/issues/219.
  [hannosch]

- Fixed the language selector to work directly on the root in a virtual hosting
  environment. This closes http://plone.org/products/linguaplone/issues/216.
  [hannosch]

- Expanded the development buildout to include a simple Nginx configuration to
  make it easier to test virtual hosting issues.
  [hannosch]

- Changed the language selector to use the canonical_object_url instead of the
  view_url. We preserve the /view postfix ourselves, so using view_url would
  duplicate this in certain situations. We also stopped doing the default page
  analysis ourselves and use the given feature from the context state view.
  [hannosch]

3.0b7 - 2009-10-21
------------------

- Protect the LanguageIndependentFields adapter against weird fields, like
  computed fields.
  [hannosch]

3.0b6 - 2009-10-20
------------------

- Avoid preserving the mysterious `-C` in the language selector.
  [hannosch]

- Made sure that subclasses of fields listed in I18NAWARE_REFERENCE_FIELDS
  also get the special reference handling. Otherwise schemaextender fields
  won't get the behavior.
  [hannosch]

- Let the `generatedMutatorWrapper` work directly on schemaextender fields.
  [hannosch]

- Replaced `has_key` with `in` checks using the `__contains__` protocol.
  [hannosch]

- Factored out generated methods from the language independent ClassGenerator
  into module scope functions to allow outside access to them.
  [hannosch]

3.0b5 - 2009-10-14
------------------

- Optimized the getTranslations method by allowing the calling functions to
  pass in a hint about the canonical status of self. Often this is known by
  the caller and doesn't have to be determined inside the getTranslations call.
  Also optimized getNonCanonicalTranslations by extending the API of
  getTranslations with a include_canonical flag.
  [hannosch]

- Optimized the getCanonical method to avoid two identical reference catalog
  queries and just do the query once.
  [hannosch]

- Added tests for and fixed more edge cases for the reference handling.
  There's about seventeen different ways how this API can be called.
  [hannosch]

- Fixed a bug in the LanguageIndependentFields adapter. It did a whole lot of
  magic to be LinguaPlone aware, just to miss the whole point. Simple is
  sometimes better. This fixes the last reference handling test failure.
  [hannosch]

- Fixed the whole references handling. Prior it used the saved references for
  synchronization, with the effect of ignoring new refs. Now it uses actually
  the given new values and looks up them. It deals now with partly translated
  targets and non-translatable targets. Also I cleaned up this part of the
  code.
  [jensens]

3.0b4 - 2009-10-02
------------------

- Fixed a serious bug that showed itself with multi valued reference fields and
  archetypes.referencebrowserwidget. Since we render language independent
  fields on the translate_item view in view mode, their data wasn't part of the
  request anymore. Omitting a field from the request is considered equivalent
  to "delete all" by processForm. We now override _processForm to ignore
  language independent fields in processForm on canonical items. This also
  gives a bit of a speed advantage.
  [hannosch]

- LinguaPlone didn't allow manual editing of IDs. Thanks to David Hostetler
  for the patch. This closes http://plone.org/products/linguaplone/issues/70.
  [hannosch]

- Removed dubious performance optimization in tests. Don't delete the catalog.
  [hannosch]

- Removed bogus license headers from Python files. All code is owned by the
  Plone Foundation and licensed under the GPL.
  [hannosch]

3.0b3 - 2009-09-26
------------------

- Update the requirement to Plone 3.3 instead of individual packages. We don't
  test this version against former Plone versions anymore. Removed no longer
  required code for pre-Plone 3.1.
  [hannosch]

- If no item was selected in the link translations form, a random item was
  selected in the form handler. Thanks to Ichim Tiberiu for the patch. This
  closes http://plone.org/products/linguaplone/issues/204.
  [hannosch]

- Restored the proper functionality of the change language function on the
  manage_translations_form. This closes
  http://plone.org/products/linguaplone/issues/215.
  [hannosch]

- Added a simple configuration option to hide the right column on the
  translation edit form and enable it by default.
  [hannosch]

- Removed the canonical and translations cache. It was never completely save
  to use. This closes http://plone.org/products/linguaplone/issues/82.
  [hannosch]

- Added a new synchronized language vocabulary and use it for the content and
  metadata language availability. This restricts the languages in the common
  language widgets to the set of the supported languages of the site.
  [hannosch]

- Removed the unmaintained support for using the Kupu reference browser in the
  manage_translations_form.
  [hannosch]

- Fixed a deprecation warning for the isRightToLeft script, which is used in
  the translationbrower_popup.
  [hannosch]

- Removed the GlobalRequestPatch - it is no longer required.
  [hannosch]

- Removed the `not_available_lang` template. It wasn't used anymore.
  [hannosch]

- Use request negotiation by default.
  [hannosch]

- Turn on the content language negotiator by default.
  [hannosch]

- Avoid a space after the language name in the selector.
  [hannosch]

- Modernized the code of the language index export import handler.
  [hannosch]

- Refactored common functionality of the catalog exportimport handlers. Added
  automatic reindexing for newly added indexes.
  [hannosch]

- Rearranged the package documentation to the top-level of the distribution.
  [hannosch]

- Added a buildout configuration to the package for stand-alone testing.
  [hannosch]

- Fixed bad spelling in status message in translate view.
  [hannosch]

- Make sure to use the native language name in the language selector in the
  same way Plone itself does this.
  [hannosch]

- Specify an alt text on the language selector images. This closes
  http://plone.org/products/linguaplone/issues/188.
  [hannosch]

- Fixed invalid code instructions in the README. This closes
  http://plone.org/products/linguaplone/issues/207.
  [hannosch]

- Removed the long broken portlet_languages. This was a pre-Plone 3 old-style
  portlet. See http://plone.org/products/linguaplone/issues/209.
  [hannosch]

3.0b2 - 2009-09-25
------------------

- Don't forget the rest of the formvariables, when dealing with request.form.
  [tesdal]

3.0b1 - 2009-09-25
------------------

- Don't mangle request.form when allowing Unicode.
  [tesdal]

- Get default language from content parent inside portal factory.
  [tesdal]

- Added dynamic id attribute to <tr> in translate_item.cpt for easier styling.
  [jensens, hpeteragitator]

3.0a3 - 2009-09-09
------------------

- Allow Unicode in request.form.
  [tesdal]

3.0a2 - 2009-09-07
------------------

- Preserve view, template and query components when switching language
  [tesdal]

- Ensure that the LinguaPlone browser layer is more specific than the default
  in the interface __iro__ so that registrations to the LinguaPlone layer win.
  [rossp]

- Added undeclared dependency on Products.PloneLanguageTool >= 3.0.
  [hannosch]

3.0a1 - 2009-06-03
------------------

- Removed `checkVersion` check from our init method and declare a dependency
  on Plone instead.
  [hannosch]

- Changed the profile version to a simple `3`, to follow best practices of
  using simple integers for profile version numbers.
  [hannosch]

- Extended multi-lingual aware reference fields to handle multi-valued fields.
  [hannosch]

- Added test for language independent lines fields.
  [hannosch]

- Fixed the testSelector tests to work with the new default page handling.
  [hannosch]

- Cleaned up some old package metadata and converted zLOG usage to logging.
  [hannosch]

- Changed the language selector to respect default pages. We now link to the
  container of the translated default page rather than the default page itself.
  [hannosch]

- Added Language as an additional index to the uid catalog. This is required
  to get at least normal reference criteria to be able to restrict their
  selections based on the language.
  [hannosch]

- Adjust the copyField methods of the LanguageIndependentFields adapter to
  work with fields which have no accessor methods.
  [hannosch]

- Reworked the translationOf reference handling. Instead of relying on the
  normal Archetypes reference API, we digg into some of the internals to
  optimize the handling for the specific use-case we have:

  * We added Language as additional metadata to the reference catalog. To do
    so we needed to add a GenericSetup handler for the catalog to this package
    for now. This should be moved to Archetypes itself. An upgrade step for
    existing sites is available and needs to be run. The step is advertised in
    the add-on control panel of Plone 3.3 and later or available via the
    portal_setup tool in the ZMI.

    The new metadata reflects the language of the source of the reference, so
    we index the translation languages and not the canonical language. So a
    reference inside the at_references folder of a translation, stores the
    Language of that translation. It gets it via Acquisition, since neither the
    reference nor the at_references OFS.Folder has a Language function.

  * As a second step we use this new metadata to more efficiently query the
    reference catalog. In general we avoid getting the real objects where
    possible and rely on the catalog internal brains to get all relevant
    information. We also bypass getting the actual reference object and
    instead look up the source or target of the reference directly by their
    uid.

  These changes do not change external API's nor should they cause problems
  for other add-ons using the reference engine.
  [hannosch]

- Split the canonical status caching of CACHE_TRANSLATIONS into its own config
  setting via CACHE_CANONICAL.
  [hannosch]

- Fixed the language selector tests to pass in Plone 3.3.
  [hannosch]

- Removed empty translation from translate menu description.
  [hannosch, maurits]

- Added smarter handling of language independent reference fields. If a
  language independent reference field points to a target, the translations of
  that source item will point to the translations of the target and not the
  canonical target. This will only work if the translations of the target
  already exist once the reference is established. If translations of the
  target are later added, the canonical source needs to be saved again to
  adjust the references to the right translation of the target.
  [hannosch]

- Added tests for language in-/dependent reference fields.
  [hannosch]

- Allow the query keys which prevent the automatic addition of the language to
  catalog queries be configured through a NOFILTERKEYS list in config.
  [hannosch]

2.4 - 2008-12-09
----------------

- Removed `Language settings` from the `Translate into` menu. A global action
  has no place in a context specific menu.
  [hannosch]

- Remove the useless 'changeLanguage' script. In
  'manage_translations_form', use '@@translate' instead.
  [nouri]

- Allow 'id' to be passed to addTranslation/createTranslation.
  [nouri]

2.3 - 2008-11-13
----------------

- Registered NoCopyReferenceAdapter for translationOf relations on
  iterate checkout to avoid the checked out object becoming the
  translation.
  [tesdal]

- Fixed unneeded AlreadyTranslated exception during a schema update.
  A schema update saves the current value, sets the default language
  (at which point there can easily be two English translations if that
  is the default language) and restores the original value again. So
  really there is no reason for doing anything other than setting the
  value in that case.
  [maurits]

- addTranslation now returns the newly created translation.
  [wichert]

- Include the FAQ in the package description.
  [wichert]

- Refactor addTranslation: introduce adapters to determine where
  a translation should be created and to create the translation.
  [wichert]

- Add path filter in catalog view, like the non-LP version has.
  [mj]

- Ensure that translations are reindexed when processing an edit form;
  language independent fields may have been updated.
  [mj]

- Extracted ILanguageIndependentFields adapter, encapsulating the
  synchronization of language independent fields.
  [stefan]

2.2 - 2008-07-22
----------------

- LanguageIndependent fields are now shown in view mode for the translations,
  so they no longer are editable from the translations, which is how it's
  documented to behave. [regebro]

- Made the upgrade step also work on Plone 3 (GenericSetup 1.3).
  [maurits]

- Registered GenericSetup upgrade step to get rid of an old
  linguaplone_various import step.  I registered it for upgrading
  from 2.0 to 2.1 as that was when this import step was removed.  It
  is always available in portal_setup/manage_upgrades in the ZMI.
  [maurits]

- When going to the canonical translation, also switch to that
  language.  [maurits]

- On the manage_translations page do not show the form for linking to
  other content or deleting/unlinking existing translations when the
  current context is not the canonical language.  Instead add a url to
  that canonical language.  [maurits]

- When adding a translation, do not throw an error when the language
  does not exist, but display that as info and go to that existing
  translation.  I saw the 'add translation' option still for an
  already translated language, due to some caching.  [maurits]

- Ignore back reference when it is None.  [maurits]

- Made sure that an existing FieldIndex Language gets correctly
  replaced by our wanted LanguageIndex, instead of leaving an unusable
  index with an empty indexable attribute.  [maurits]

- Check if plone.browserlayer is installed before starting a possibly
  long reindex that would then be aborted.  [maurits]

- Make tests run on Plone 3.0.6 with plone.browserlayer 1.0rc3 and
  original GenericSetup (1.3) next to simply Plone 3.1.  [maurits]

2.1.1 - 2008-05-01
------------------

- Removed the dependency on the no longer existing plone.browserlayer
  GS profile. This closes http://dev.plone.org/plone/ticket/8083.
  [hannosch]

- Add a workaround Plone bug #8028 (http://dev.plone.org/plone/ticket/8028)
  which causes site errors in contexts without a portal_type, such as
  the portlet add form.
  [wichert]

2.1 - 2008-04-11
----------------

- Use our language selector viewlet for all content types instead of just
  translatable types. This makes things consistent for all types.
  [wichert]

- Be more tolerant in unindexing non-existent content.
  [hannosch]

- Allow languages to be unselected in the language control panel.
  [wichert]

- Do not use LanguageDropdownChoiceWidget for the default language field
  in the control panel: LanguageDropdownChoiceWidget uses
  IUserPreferredLanguages, which does not use the proper vocabularies to
  find the language names.
  [wichert]

2.1beta1 - 2008-04-07
---------------------

- Register the LanguageIndex with the selection widget, so you can query
  for languages in Collections.
  [hannosch]

- Enable the Plone language portlet and change its rendering link
  correctly to translations if they exist and to the site root
  otherwise.
  [wichert]

- Dont depend on Quickinstaller at setup time and in browsermenu.
  [jensens]

- Minor GenericSetup cleanup
  [jensens]

- Make LinguaPlone play nice with archetypes.schemaextender and
  similar approaches.
  [jensens]

- Declare plone.browserlayer as a dependency in our GenericSetup profile.
  This will automatically install it in Plone 3.1.
  [wichert]

- Better unlink handling. This fixes
  http://plone.org/products/linguaplone/issues/127
  [wichert]

2.1alpha1 - 2007-12-13
----------------------

- Refuse to install LinguaPlone of plone.browserlayer is not already
  installed.
  [wichert]

- Register the PloneLanguageTool GenericSetup export/import steps in
  LinguaPlone as well.  Standard Plone 3 installs never applied the
  PloneLanguageTool GenericSetup context, so without this
  portal_languages.xml would be ignored.
  [wichert]

- Replace the standard Plone language control panel with our own version
  which allows enabling of multiple languages.
  [wichert]

- Manage translations form now uses a kupu drawer when the kupu
  reference browser is enabled. [Duncan]

- Actions from the manage translations screen now stay on that
  screen so multiple translations may be linked. Existing
  translations display their path. [Duncan]

2.0 - 2007-10-11
----------------

- When creating new content in a translated parent use the language of
  the parent as the default language.
  [wichert]

- Try to unlock objects before moving them into a newly translated folder.
  [wichert]

- Add a test in the GS various import step if the Language catalog index
  in portal_catalog has indexed any objects. If not we just (re)created
  the index and we need to reindex it. This fixes content disappearing
  after installing LinguaPlone.
  [wichert]

- Remove the code to mark LinguaPlone as installed in the quickinstaller
  from the GS profile: we can install LinguaPlone through the quickinstaller
  itself so this is not needed.
  [wichert]

2.0beta2 - 2007-09-24
---------------------

- Fix a syntax error in the translate_item template.
  [wichert]

- Restructure the LinguaPlone product layout so it can be distributed
  as an egg.
  [wichert]

2.0beta1 - 2007-09-21
---------------------

- Allow translating the default view for an untranslated container
  again: we have correct code that adds a translation of the container
  as well now.
  [wichert]

- Correct creationg of translations for objects which are the default
  view of a non-translatable parent.
  [wichert]

- Correct handling of the translate into-menu for content with an
  untranslatable parent.
  [wichert]

2.0alpha2 - 2007-09-19
----------------------

- Only show the content menu if LinguaPlone is installed in the quick
  installer.
  [wichert]

- Update functional tests to login as a member so the test can use unpublished
  content.
  [mj]

- Disable the menu option to translate the default view for a folder to a
  language for which the folder has no translation.
  [wichert]

2.0alpha1 - 2007-09-10
----------------------

- Use a GenericSetup profile to install LinguaPlone.
  [wichert]

- Move createTranslations to a @@translate browser view.
  [wichert]

- Port to Plone 3.0.1.
  [wichert]

- Only allow linking to other objects of the same portal type.
  [wichert]

- Add a sanity to prevent addTranslationReference from adding translations
  for languages which already have a translation.
  [wichert]

- Policy change for language selector. We try to avoid disabled flags by
  looking for a translated parent.
  [fschulze]

- Added UI to link translations together.
  [vlado, fschulze]

- Changed to use _createObjectByType on addTranslation, bypassing possible
  conflicts with adding restrictions.
  [deo]

1.0.1 - 2007-09-24
------------------

- Fix spitLanguage to return (None, None) when fed a non-string object.
  This fixes LP issue #101.
  [mj]

- Fix LanguageIndex to deal better with objects where Language is either
  missing or not a callable. Fixes LP issue #99.
  [mj]

- Fix LanguageIndex to run on python 2.3.
  [wichert]

- Fix language selector to not go the the login screen if one of the
  translations is not accessible (i.e. in "private" state)
  [fschulze, godchap]

1.0 - 2007-06-19
----------------

- If we are resetting the language due to a schema update do not delete the
  translation references. This fixes
  http://plone.org/products/linguaplone/issues/7
  [wichert]

- Removed Plone 2.0 compatibility.
  [fschulze]

- Add a utility method to link content objects as translations. This
  is useful, for example, in a GenericSetup import step to link content
  created in a GenericSetup content step.
  [wichert]

- Show the 'Switch language to' text in the language selector in the
  target language instead of the current language.
  [wichert]

- Fixed so rename after creation only happend on TTW creation. Not on
  first edit of a through script created object.
  [sashav]

- Fixed an issue if theres no getTranslations available. This happens if
  an non-lp-enabled at-based object exists direct in portal-object.
  [jensens]

- Fixed some code that spit out DeprecationWarnings.
  [hannosch]

- Instead of customizing switchLanguage we now have portlet_languages
  inside LinguaPlone and use the much nicer languageSelectorData.
  [jladage]

- LanguageIndex is now a specialised index that will return alternative
  translations within the main language when searching.
  [mj]

0.9.0 - 2006-06-16
------------------

- Now works with Plone 2.5 out-of-the-box, and Plone 2.1.3 if using the
  included PloneLanguageTool.

- Fixed unicode error on translated languages in Plone 2.1.3. It can
  contains non-ascii characters, so the default strings need to be
  declared as unicode.
  [encolpe]

- Fixed actions to fallback gracefully for the action attribute 'name'
  and 'title'.
  [jladage] [encolpe]

- Added the switchLanguage.py script and added support for translatable
  content.
  [jladage]

- Fixed to lookup the language flag name directly from the language tool.
  Now, PloneLanguageTool 1.3 (or greater) is officially required.
  [deo]

- Made tests compatible with Plone 2.5.
  [hannosch]

- Some very minor i18n fixes.
  [hannosch]

- Added a migration script to update language independent fields content.
  It *must* be manually run when upgrading from versions older than 0.9.
  [deo]

- Removed the custom accessor/editAccessor generation. We're only using
  custom mutators and translation mutators for now. This result in a ~30%
  performance improvement over the previous versions.
  [deo]

- Made sure to copy independent language fields data to all translations
  as we removed the custom accessor. This also fixed the problem when
  you try to get values direct from fields, as now the data is in the
  translations too, not only in the canonical object.
  [deo]

- Forwared fix for http://dev.plone.org/plone/ticket/4939.
  [deo]

- Fixed a problem when switching between translations of images/files,
  where the content was shown, instead of the view screen.
  [deo]

- Fixed to highlight the 'Edit' tab from a translation when you click it.
  [deo]

- Final cut on Plone 2.0 compatibility. Backported tests, handled
  migrations and patched tool with the PythonScripts content.
  [deo] [sidnei]

- Added labels to language-independent fields.
  [deo] [limi]

- Made the initial default language follow the PloneLanguageTool config
  policy.
  [deo]

0.9-beta - 2005-10-27
---------------------

- Removed content border from Translation Unavailable template.
  [limi]

- Made the test fields that are not editable render in view mode, not as
  non-editable text boxes. The reasons for this are that people tend to
  think that "if it is a text box, it's editable", and are then confused
  when it's not (read-only widgets confuse the heck out of users), and the
  other reason is because it messes up multiple selection lists.
  [limi]

- Made language-independent items not editable in a translation.
  [limi] [deo]

- Added first cut on Plone 2.0 compatibility.
  [deo]

- Fixed i18n domain everywhere... :-)
  [deo]

0.8.5 - 2005-09-06
------------------

- Made content be created in neutral language, now that this concept
  works as expected.
  [deo]

- Made addTranslation raise an AlreadyTranslated exception when trying
  to duplicate a translation.
  [deo]

- Added form to create translation when the language don't exist and
  if the user has the appropriate permissions.
  [deo]

- Title on the flag switcher should say: "Switch language to $LANGUAGE
  (content translation not available)" - the last part if the content
  is not translated, to complement the ghosting (which is purely visual,
  and bad for accessibility).
  [deo]

- Split screen should change sides ("From" language to the left, "To"
  language to the right).
  [deo]

- Split screen should not show short name if turned off (like the
  default is in 2.1).
  [deo]

- Flags aren't on a separate line anymore (they used to be below the
  document actions).
  [limi]

- Field titles are translated, field help is not.
  [deo]

- Flags should probably be removed from the field titles, since the
  pulldown might make these misleading.
  [deo]

- Split-screen pulldown needs language selectors when translating.
  [deo]

- Use the translate_item template when editing translatable content,
  except the canonical one.
  [deo]

- PloneLanguageTool has problems without LinguaPlone installed.
  [deo]

- Added norwegian translation.
  [limi]

- Improved i18n markup. Updated brazilian portuguese translation.
  [deo]

0.8 - 2005-08-15
----------------

- Plone __browser_default__ review.
  [deo]

- Adjust LP catalog patch for Plone 2.1.
  [stefan]

- Allowed changing language of content, moving content to appropriate
  place, and raising a exception when forbidden.
  [deo]

- Design the policy for the New language negotiator.
  [limi]

- Grayed out flags.
  [deo, limi]

- Handle switching to non-existing language (a.k.a. not_available_lang).
  [deo]

- Handle translation of default pages.
  [deo]

- Added hasTranslation() method for grayed-out flags.
  [deo]

- ID policy for translating containing folder and moving translated content.
  [limi]

- Language switching: the URL on flags should be the actual URL, not
  switchLanguage?set_language=no.
  [deo]

- Fixed languageswitcher in Firefox.
  [deo]

- LinguaPlone should not append language code to ID, it should use
  the same Plone 2.1 policy.
  [deo]

- Implemented the new language negotiator, where content and interface
  languages are always in sync.
  [deo]

- Test that Images in ATCT are keeping the image LangIndependent.
  [limi]

- Update dropdown menus markup.
  [deo]

0.7 - 2004-09-24
----------------

- Released at Plone Conference 2004.
  [limi] [testal] [geir]

Technology Preview - 2004-06-29
-------------------------------

- First publicly available version.
  [limi] [testal] [geir]
