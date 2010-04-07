from zope.interface import implements
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PlacelessTranslationService import getTranslationService

from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.app.portlets.portlets import base

try:
    from osha.adaptation.subtyper import IAnnotatedLinkList
except ImportError:
    from osha.policy.adapter.subtyper import IAnnotatedLinkList

try:
    from osha.adaptation.vocabulary import AnnotatableLinkListVocabulary
except ImportError:
    from osha.theme.vocabulary import AnnotatableLinkListVocabulary

class IFOPLinksPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):

    implements(IFOPLinksPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return "FOP Links"


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('fop_links.pt')

    def link_sections(self):
        sectionid2msgid_map = {
            "authorities": "heading_authorities",
            "social_partners": "heading_social_partners",
            "other_national": "heading_other_national_sites",
            "research_organisations": "heading_research_organisations",
            "more": "heading_more_related_content",
            }
        link_section_dict = {}
        preflang = getToolByName(
            self.context, 'portal_languages'
            ).getPreferredLanguage()
        translate = getTranslationService().translate
        section_ids = dict(
            AnnotatableLinkListVocabulary().getDisplayList().items()
            )

        for id in section_ids.keys():
            msgid = sectionid2msgid_map[id]
            heading = translate(
                target_language=preflang,
                msgid=msgid,
                default=section_ids[id],
                context=self.context,
                domain="osha"
                )
            link_section_dict[id] = heading
        return link_section_dict

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        return (preflang)

    # @ram.cache(_render_cachekey)
    # TODO using the language only as a cache key isn't sufficient
    def render(self):
        return self._template()

    def has_links(self):
        """ Check if this page has been subtyped to provide annotated
        links """
        context = self.context
        return IAnnotatedLinkList.providedBy(context) and \
            context.Schema().getField('annotatedlinklist').get(context)

    def get_links_by_section(self, section):
        context = self.context
        if IAnnotatedLinkList.providedBy(self.context):
            links = context.Schema().getField('annotatedlinklist').get(context)
            return [i for i in links if i["section"] == section]
        else:
            return None

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = self.context

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IFOPLinksPortlet)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IFOPLinksPortlet)
