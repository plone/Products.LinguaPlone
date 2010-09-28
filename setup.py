from setuptools import setup, find_packages
import os.path

version = '3.2a1'

setup(name='Products.LinguaPlone',
      version=version,
      description="Manage and maintain multilingual content that integrates seamlessly with Plone.",
      long_description=".. contents::\n\n" +
                        open("README.txt").read() + "\n" +
                        open(os.path.join("docs", "FAQ.txt")).read() + "\n" +
                        open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='Zope Plone multilingual translation',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/Products.LinguaPlone',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Plone >= 3.3, <4.0dev',
        'Products.CMFCore',
        'Products.PloneLanguageTool',
        'plone.browserlayer',
        'plone.app.i18n',
        'plone.app.layout',
        'zope.component',
      ],
)
