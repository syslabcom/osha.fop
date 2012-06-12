from osha.fop.tests.base import INTEGRATION_TESTING

import unittest2 as unittest


class TestView(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_view_methods(self):
        """ Test the methods in the oshnetwork-member-view class """

        ltool = self.portal.portal_languages
        ltool.addSupportedLanguage('nl')

        view = self.portal.en.belgium.index_html.restrictedTraverse(
            "@@oshnetwork-member-view")
        view.context.setLanguage('en')
        localized_path = view.get_localized_path("asdf")
        self.assertEquals(localized_path,
                          "/en/asdf")

        # Change the language
        view.context.setLanguage("nl")
        localized_path = view.get_localized_path("asdf")
        self.assertEquals(localized_path,
                          "/nl/asdf")


def test_suite():
    """This sets up a test suite that actually runs the tests in
    the class(es) above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
