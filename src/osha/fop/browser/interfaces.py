from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IOSHNetworkMemberView(Interface):
    """Marker interface that defines a Zope 3 skin layer.
    """

    def get_localized_path(path):
        """ A method to prefix a path with the currently selected language
        string """

    def get_news(number_of_items):
        """ return the brains for relevant news items """

    def get_additional_translations():
        """
        Return translations for the current context which aren't
        available from the language selection drop down

        {"tr":("Turkish", "http://url",) ...}
        """

    def get_language_selected(lang):
        """
        For use in the selection list:

        Return "selected" if the lang matches the self.Language lang is
        "en" and self.Language is None.
        """

class IFOPSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """
