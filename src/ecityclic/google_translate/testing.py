# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ecityclic.google_translate


class EcityclicGoogleTranslateLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=ecityclic.google_translate)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ecityclic.google_translate:default')


ECITYCLIC_GOOGLE_TRANSLATE_FIXTURE = EcityclicGoogleTranslateLayer()


ECITYCLIC_GOOGLE_TRANSLATE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ECITYCLIC_GOOGLE_TRANSLATE_FIXTURE,),
    name='EcityclicGoogleTranslateLayer:IntegrationTesting',
)


ECITYCLIC_GOOGLE_TRANSLATE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ECITYCLIC_GOOGLE_TRANSLATE_FIXTURE,),
    name='EcityclicGoogleTranslateLayer:FunctionalTesting',
)


ECITYCLIC_GOOGLE_TRANSLATE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ECITYCLIC_GOOGLE_TRANSLATE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EcityclicGoogleTranslateLayer:AcceptanceTesting',
)
