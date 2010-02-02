"""
FOP/OSHA Network Member specific viewlets
"""

from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.LinguaPlone.interfaces import ITranslatable
from zope.component import queryMultiAdapter

from osha.theme.browser.viewlets import OSHALanguageSelector

class MoreLanguagesViewlet(OSHALanguageSelector):
    """
    Methods to get the available translations of the current object
    which aren't included in the global language selection tool.
    """
    render = ViewPageTemplateFile('morelanguages.pt')

    def get_additional_translations(self):
        """
        Return translations for the current context which aren't
        available from the language selection drop down

        {"tr":("Turkish", "http://url",) ...}
        """
        context = self.context
        portal_langs = [i["code"] for i in self.languages()]

        translatable = ITranslatable(context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = {}

        additional_translations = {}
        portal_state = queryMultiAdapter((context, self.request),
                                         name=u'plone_portal_state')
        lang_names = portal_state.locale().displayNames.languages
        lang_codes = [i for i in translations.keys() if i not in portal_langs
            and i != ""]
        can_edit = getSecurityManager().checkPermission(
                permissions.ModifyPortalContent,
                context
                )

        for lang_code in lang_codes:
            is_published = translations[lang_code][1] == "published"
            if can_edit or is_published:
                additional_translations[lang_code] = \
                    (lang_names[lang_code],
                     translations[lang_code][0].absolute_url(),)
        return additional_translations

    def get_language_selected(self, lang):
        """
        For use in the selection list:

        Return "selected" if the lang matches the self.Language lang is
        "en" and self.Language is None.
        """
        selected = ""
        obj_lang = self.context.Language()
        if lang == obj_lang or\
             lang == "en" and obj_lang == "":
            selected = "selected"
        return selected
