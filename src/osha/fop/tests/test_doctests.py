import doctest
import unittest2 as unittest

from osha.fop.tests.base import FUNCTIONAL_TESTING
from plone.testing import layered

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite  = unittest.TestSuite()
    suite.addTests([
            layered(
                doctest.DocFileSuite(
                    "oshnetwork_member_view.txt", optionflags=OPTIONFLAGS),
                layer=FUNCTIONAL_TESTING),
            ])
    return suite
