"""
Some Focal Points have a full subsite in addition to this FOP
section. This portlet provides a link to such a site.
"""

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PlacelessTranslationService import getTranslationService
from plone.portlets.constants import CONTEXT_CATEGORY

from plone.app.portlets.portlets import base
from plone.app.portlets.utils import assignment_mapping_from_key
from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider


class IFOPMainPromotionPortlet(IPortletDataProvider):
    """
    The url to the main Focal Point site is set on the portlet in the
    canonical translation.
    """
    url = schema.TextLine(
        title=_(u'URL of the Main Site for this Focal Point'),
        description=_(
        u"""Enter the url to the main Focal Point site for this member
        state"""),
        required=True,
        )

class Assignment(base.Assignment):
    """
    Configuration class
    """
    implements(IFOPMainPromotionPortlet)

    def __init__(self, url):
        self.url = url

    @property
    def title(self):
        return "FOP Main Site"


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('fop_main_promotion.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = self.context

    def _render_cachekey(method, self):
        preflang = getToolByName(
            self.context, 'portal_languages'
            ).getPreferredLanguage()
        return (preflang)

    @ram.cache(_render_cachekey)
    def render(self):
        return self._template()

    def url(self):
        """
        Return the url to the main FOP site for this member state

        This is set on the canonical member state only
        """
        context = self.context
        request = self.request
        osha_view = getMultiAdapter((context, request), name=u'oshaview')
        subsite_root = context.restrictedTraverse(osha_view.subsiteRootPath())
        canonical_member_state = self.subsite_root.getCanonical()
        try:
            right_portlets = assignment_mapping_from_key(
                canonical_member_state, 'plone.rightcolumn', CONTEXT_CATEGORY,
                "/".join(canonical_member_state.getPhysicalPath())
                )
        except ComponentLookupError:
            return
        if "fop-main-site" in right_portlets.keys():
            return right_portlets["fop-main-site"].url


    @memoize
    def heading_main_fop_portlet(self):
        """
        Return the a heading for this focal point in the current
        language.
        """
        context = self.context
        request = self.request
        osha_view = getMultiAdapter((context, request), name=u'oshaview')
        subsite_root = context.restrictedTraverse(osha_view.subsiteRootPath())
        preflang = getToolByName(
            context, 'portal_languages'
            ).getPreferredLanguage()
        translate = getTranslationService().translate
        msgid = "heading_main_fop_portlet_%s" % subsite_root.getId()
        heading = translate(
            target_language=preflang,
            msgid=msgid,
            default="Main Focal Point",
            context=context,
            domain="osha"
            )
        return heading


class AddForm(base.AddForm):
    """ Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IFOPMainPromotionPortlet)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IFOPMainPromotionPortlet)
    label = _(u"Edit FOP Main Site Portlet")
    description = _(u"This portlet displays a link to the main FOP site.")
