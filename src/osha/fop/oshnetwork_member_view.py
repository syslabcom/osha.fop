from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.LinguaPlone.interfaces import ITranslatable
from plone.app.i18n.locales.browser.selector import LanguageSelector
from zope.app.component.hooks import getSite
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import implements

from osha.fop.interfaces import IOSHNetworkMemberView


class OSHNetworkMemberView(BrowserView):
    """
    Browser view for oshnetwork-member-view
    """
    implements(IOSHNetworkMemberView)

    template = ViewPageTemplateFile("oshnetwork_member_view.pt")
    template.id = "oshnetwork-member-view"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []
        self.request.set('disable_border', True)
        self.language = context.Language()

    def __call__(self):
        return self.template()

    def get_localized_path(self, path):
        """
        A method to prefix a path with the currently selected language
        string.
        """
        context = self.context
        language = context.Language()
        # Remove any '/' from the start of the path
        path = path.lstrip("/")
        return "/%s/%s" % (language, path)

    def get_national_flag(self):
        """
        Return the image tag for the national flag of the member
        state.
        """
        context = self.context
        country = context.aq_inner.aq_parent.getId()
        flag = country + "_large.gif"
        try:
            img = context.restrictedTraverse(flag)
            flag_tag = img.tag()
        except AttributeError:
            flag_tag = ""

        return flag_tag

    def get_news(self):
        """ return the brains for relevant news items """
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        language = context.Language()
        now = DateTime()
        query = dict(portal_type='News Item',
                     review_state='published',
                     effective={'query': now,
                          'range': 'max'},
                     expires={'query': now,
                          'range': 'min'},
                     sort_on='effective',
                     sort_order='reverse',
                     Language=language)

        brains = catalog(query)
        return brains

    def get_fop_translations(self):
        """
        Return the available translations for the current context

        {"nl":("Dutch", "http://url",) ...}
        """
        translatable = ITranslatable(self.context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

        available_translations = {}
        portal_state = queryMultiAdapter((self.context, self.request),
                                         name=u'plone_portal_state')
        lang_names = portal_state.locale().displayNames.languages
        for lang_code in translations.keys():
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
        obj_lang = self.language
        if lang == obj_lang or\
             lang == "en" and obj_lang == "":
            selected = "selected"
        return selected
