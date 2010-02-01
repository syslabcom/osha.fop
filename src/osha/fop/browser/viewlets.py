"""
FOP/OSHA Network Member specific viewlets
"""

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

    def get_available_translations(self):
        """
        Return the available translations for the current context

        {"nl":("Dutch", "http://url",) ...}
        """
        context = self.context
        portal_langs = [i["code"] for i in self.languages()]

        translatable = ITranslatable(context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = {}

        available_translations = {}
        portal_state = queryMultiAdapter((context, self.request),
                                         name=u'plone_portal_state')
        lang_names = portal_state.locale().displayNames.languages
        lang_codes = [i for i in translations.keys() if i not in portal_langs
            and i != ""]
        for lang_code in lang_codes:
            if translations[lang_code][1] == "published":
                available_translations[lang_code] = \
                    (lang_names[lang_code],
                     translations[lang_code][0].absolute_url(),)
        return available_translations

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
