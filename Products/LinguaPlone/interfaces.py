# Jarn AS <info@jarn.com>
# Martijn Pieters <mj@jarn.com>
# http://www.jarn.com

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from zope.interface import Attribute
from zope.interface import Interface

from Products.PluginIndexes.interfaces import IPluggableIndex

class ILinguaPloneProductLayer(Interface):
    """A layer specific for LinguaPlone.

    We will use this to register browser pages that should only be used
    when LinguaPlone is installed in the site.
    """


class ILanguageIndex(IPluggableIndex):
    """Index for ITranslatable Language tags
    
    The index treats language tags according to RFC 1766, with the assumption
    that languages with more than one subtag but with the same initial subtag 
    as related; en-us is related to en-gb, and will fall back to related
    content (same canonical UID) when queried.
    
    Language tags are treated as containing a initial subtag, and one optional
    second subtag, splitting a tag on the first dash. Thus, this index does
    not support additional subtags, but modern browsers never send anything 
    more complicated than a main language with a region or dialect, nor do
    current Plone i18n tools support anything else.
    
    Fallback rules are as follows: if searching for a given language tag, a 
    union is returned of:
    
    1. Exact tag match
    2. Initial subtag match, no second subtag (if not the original search)
    3. Any other second subtags indexed for the initial subtag in alfabetical
       order.
    
    Results are filtered for unique canonical UIDs, thus ensuring only one
    translation per content item is returned.
    
    So, when searching for en-gb, all matches for en-gb are returned, plus
    any matches for en, en-au, en-ca, en-nz, en-us if such tags were indexed
    and not already translated into en-gb.
    
    The fallback behaviour can be disabled by setting index.fallback to False,
    or passing a 'fallback' query parameter (also a boolean) to the index
    when querying.

    """
    
    fallback = Attribute(
        'fallback',
        """Wether or not to enable language fallback querying.
        
        Boolean, defaults to True.
        """,
        )

class ITranslatable(Interface):
    """
    Interface for translatable content.

    This was originally a Zope2 interface in CMFPlone:
    Products.CMFPlone.interfaces.Translatable.ITranslatable.
    """

    def isTranslation():
        """
        return language if this object is used as multilingual content, 0 otherwise
        """

    def addTranslation(language, **kwargs):
        """
        Add a new language translation of this content.
        """

    def removeTranslation(language):
        """
        Removes a translation
        """

    def getTranslation(language='language'):
        """
        Return the object corresponding to a translated version or None.
        If called without arguments it returns the translation in the currently
        selected language, or self.
        """
 
    def getTranslationLanguages():
        """
        Return a list of language codes
        """

    def getTranslations():
        """
        Return a dict of {lang : [object, wf_state]}
        """

    def isCanonical():
        """
        boolean, is this the original, canonical translation of the content.
        """

    def getCanonicalLanguage():
        """
        Return the language code for the canonical translation of this content.
        """

    def getCanonical():
        """
        Return the original, canonical translation of this content.
        """

    def setLanguage(language):
        """
        Sets the language for the current translation - same as DC
        """

    def Language():
        """
        Returns the language of this translation - same as DC
        """
