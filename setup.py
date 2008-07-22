from setuptools import setup, find_packages

version = '2.0'

setup(name='Products.LinguaPlone',
      version=version,
      description="LinguaPlone is a tool to manage and maintain multilingual content that integrates seamlessly with Plone.",
      long_description=open('Products/LinguaPlone/README.txt').read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
      ],
      keywords='Zope CMF Plone multilingual translation',
      author='Plone Solutions',
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
      ],
)
