# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone.app.testing import TEST_USER_ID, setRoles

from plone import api
from plone.passwordless.testing import (  # noqa: E501
    PLONE_PASSWORDLESS_INTEGRATION_TESTING,
)

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that plone.passwordless is properly installed."""

    layer = PLONE_PASSWORDLESS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plone.passwordless is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'plone.passwordless'))

    def test_browserlayer(self):
        """Test that IPlonePasswordlessLayer is registered."""
        from plone.browserlayer import utils

        from plone.passwordless.interfaces import IPlonePasswordlessLayer
        self.assertIn(
            IPlonePasswordlessLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PLONE_PASSWORDLESS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('plone.passwordless')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if plone.passwordless is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'plone.passwordless'))

    def test_browserlayer_removed(self):
        """Test that IPlonePasswordlessLayer is removed."""
        from plone.browserlayer import utils

        from plone.passwordless.interfaces import IPlonePasswordlessLayer
        self.assertNotIn(IPlonePasswordlessLayer, utils.registered_layers())
