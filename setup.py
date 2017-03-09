from setuptools import setup, find_packages
import os.path

version = '4.2'

setup(
    name='Products.LinguaPlone',
    version=version,
    description="Manage and maintain multilingual content that integrates "
                "seamlessly with Plone.",
    long_description=(
        ".. contents::\n\n" +
        open("README.rst").read() + "\n" +
        open(os.path.join("docs", "FAQ.txt")).read() + "\n" +
        open("CHANGES.rst").read()),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Zope Plone multilingual translation',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.python.org/pypi/Products.LinguaPlone',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      'setuptools',
      'AccessControl',
      'Acquisition',
      'DateTime',
      'Missing',
      'Products.Archetypes',
      'Products.ATContentTypes >= 2.0.2',
      'Products.CMFCore',
      'Products.CMFDynamicViewFTI',
      'Products.CMFPlone',
      'Products.GenericSetup',
      'Products.PloneLanguageTool',
      'Products.PloneTestCase',
      'Products.statusmessages',
      'Products.ZCTextIndex',
      'ZODB3',
      'Zope2 >= 2.12.5',
      'plone.browserlayer',
      'plone.i18n',
      'plone.indexer',
      'plone.locking',
      'plone.memoize',
      'plone.theme',
      'plone.app.caching',
      'plone.app.controlpanel >= 2.1',
      'plone.app.i18n >= 2.0.1',
      'plone.app.iterate',
      'plone.app.layout',
      'plone.app.portlets',
      'zope.component',
      'zope.formlib',
      'zope.i18nmessageid',
      'zope.interface',
      'zope.schema',
      'zope.site',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
)
