from zope.interface import Interface

class IOSHNetworkMemberView(Interface):
    """Marker interface that defines a Zope 3 skin layer.
    """

    def get_localized_path(path):
        """ A method to prefix a path with the currently selected language
        string """

    def get_news(number_of_items):
        """ return the brains for relevant news items """

    def get_available_translations():
        """
        Return the available translations for the current context

        {"nl":("Dutch", "http://url",) ...}
        """

    def get_language_selected(lang):
        """
        For use in the selection list:

        Return "selected" if the lang matches the self.Language lang is
        "en" and self.Language is None.
        """
