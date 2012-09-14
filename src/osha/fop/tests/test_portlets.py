from osha.fop.tests.base import INTEGRATION_TESTING
from osha.fop.portlets import fop_links
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping
from zope.component import getUtility, getMultiAdapter

import unittest2 as unittest


class TestFopLinksPortlet(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.folder = self.portal['folder']

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='osha.FOPLinks')
        self.assertEquals(portlet.addview,
            'osha.FOPLinks')

    def test_interfaces(self):
        portlet = fop_links.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='osha.FOPLinks')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   fop_links.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = fop_links.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, fop_links.EditForm))

    def get_renderer(self, obj):
        request = obj.REQUEST
        view = obj.restrictedTraverse('@@oshnetwork-member-view')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=obj)
        assignment = fop_links.Assignment()

        return getMultiAdapter(
            (obj, request, view, manager, assignment), IPortletRenderer)

    def test_obtain_renderer(self):
        renderer = self.get_renderer(self.portal.en.belgium.index_html)
        self.failUnless(isinstance(renderer, fop_links.Renderer))

    def test_fallback_links(self):
        fop_en = self.portal.en.belgium.index_html
        fop_de = self.portal.en.belgium["index_html-de"]
        fop_en_portlet = self.get_renderer(fop_en)
        fop_de_portlet = self.get_renderer(fop_de)
        self.assertEqual(fop_de.annotatedlinklist, ())
        self.assertNotEqual(fop_en.annotatedlinklist, ())
        self.assertEqual(fop_de_portlet.links, fop_en.annotatedlinklist)


def test_suite():
    """This sets up a test suite that actually runs the tests in
    the class(es) above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

