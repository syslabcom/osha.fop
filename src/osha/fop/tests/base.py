from zope.interface import alsoProvides

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.testing import z2

from osha.adaptation.subtyper import IAnnotatedLinkList


class OshaFop(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import osha.fop
        self.loadZCML('configure.zcml', package=osha.fop)
        import p4a.subtyper
        self.loadZCML('configure.zcml', package=p4a.subtyper)
        import osha.adaptation
        self.loadZCML('configure.zcml', package=osha.adaptation)

        z2.installProduct(app, 'osha.fop')
        z2.installProduct(app, 'p4.subtyper')
        z2.installProduct(app, 'osha.adaptation')

    def setUpPloneSite(self, portal):
        quickInstallProduct(portal, 'p4a.subtyper')
        applyProfile(portal, 'osha.fop:default')

        # Login as manager and create test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory("Folder", "folder")
        portal.invokeFactory("Folder", "en")

        # Add and configure a FOP
        portal.en.invokeFactory("Folder", "belgium")
        portal.en.belgium.invokeFactory("Document", "index_html")
        be_fop = portal.en.belgium.index_html
        be_fop.setLayout('oshnetwork-member-view')
        alsoProvides(be_fop, IAnnotatedLinkList)
        be_fop.annotatedlinklist = ({
                'url': 'http://www.employment.belgium.be/',
                'section': 'authorities',
                'linktext': 'Link Text',
                'title': 'Link Title'},)
        be_fop.addTranslation("de")
        alsoProvides(portal.en.belgium["index_html-de"], IAnnotatedLinkList)


    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'osha.fop')
        z2.uninstallProduct(app, 'p4.subtyper')
        z2.uninstallProduct(app, 'osha.adaptation')


OSHA_FOP_FIXTURE = OshaFop()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(OSHA_FOP_FIXTURE,),
    name="OshaFop:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OSHA_FOP_FIXTURE,),
    name="OshaFop:Functional")
