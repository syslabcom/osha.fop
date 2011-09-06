"""
FOP/OSHA Network Member specific browser view
"""

from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

from osha.fop.browser.interfaces import IOSHNetworkMemberView


class OSHNetworkMemberView(BrowserView):
    """
    Browser view for oshnetwork-member-view
    """
    implements(IOSHNetworkMemberView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []
        self.request.set('disable_border', True)

    def getName(self):
        return self.__name__

    def __call__(self):
        return self.index()

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
        """ Return the brains for relevant news items """
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
