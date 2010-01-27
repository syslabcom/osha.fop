import doctest
import unittest

from base import OshaFopFunctionalTestCase

from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    return unittest.TestSuite((

            Suite('tests/oshnetwork_member_view.txt',
                   optionflags=OPTIONFLAGS,
                   package='osha.fop',
                   test_class=OshaFopFunctionalTestCase) ,

        ))
