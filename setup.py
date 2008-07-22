from setuptools import setup, find_packages
import os

version = '2.1beta1'

setup(name='Products.LinguaPlone',
      version=version,
      description="Manage and maintain multilingual content that integrates seamlessly with Plone.",
      long_description=open(os.path.join("Products", "LinguaPlone", "README.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
      ],
      keywords='Zope CMF Plone multilingual translation',
      author='Jarn (formerly Plone Solutions)',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/LinguaPlone/trunk',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      download_url='http://plone.org/products/linguaplone',
      install_requires=[
        'setuptools',
        'plone.browserlayer',
      ],
)
