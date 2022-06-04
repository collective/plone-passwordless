# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    PLONE_FIXTURE,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2

import plone.passwordless


class PlonePasswordlessLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plone.passwordless)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.passwordless:default')


PLONE_PASSWORDLESS_FIXTURE = PlonePasswordlessLayer()


PLONE_PASSWORDLESS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_PASSWORDLESS_FIXTURE,),
    name='PlonePasswordlessLayer:IntegrationTesting',
)


PLONE_PASSWORDLESS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_PASSWORDLESS_FIXTURE,),
    name='PlonePasswordlessLayer:FunctionalTesting',
)


PLONE_PASSWORDLESS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_PASSWORDLESS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PlonePasswordlessLayer:AcceptanceTesting',
)
