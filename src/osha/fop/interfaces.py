from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager

from plone.app.portlets.interfaces import IColumn
from plone.theme.interfaces import IDefaultPloneLayer
from plone.portlets.interfaces import IPortletManager

_ = MessageFactory('osha.theme')


class IOSHNetworkMemberView(Interface):
    """Marker interface that defines a Zope 3 skin layer.
    """

    def get_localized_path(path):
        """ A method to prefix a path with the currently selected language
        string """

    def get_news(number_of_items):
        """ return the brains for relevant news items """

    def get_fop_languages(self):
        """ Return the languages for the current FOP
        e.g. For Belgium return "en","nl","fr"
        """
