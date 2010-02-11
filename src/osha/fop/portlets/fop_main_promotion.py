"""
Some Focal Points have a full subsite in addition to this FOP
section. This portlet provides a link to such a site.
"""

from zope.interface import implements
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from plone.app.portlets.portlets import base


class IFOPMainPromotionPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):
    """
    Configuration class
    """

    implements(IFOPMainPromotionPortlet)

    def __init__(self):
        pass

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

    #@ram.cache(_render_cachekey)
    def render(self):
        return self._template()

    def url(self):
        """
        Return the url to the main FOP site for this member state
        """
        return "http://www.member-state.eu"

    #@memoize
    def heading_focal_point(self)@:
        """
        Return the a heading for this focal point in the current
        language.
        """
        return "Belgian Focal Point"

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
