# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from ecityclic.google_translate.testing import (  # noqa: E501
    ECITYCLIC_GOOGLE_TRANSLATE_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that ecityclic.google_translate is properly installed."""

    layer = ECITYCLIC_GOOGLE_TRANSLATE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ecityclic.google_translate is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'ecityclic.google_translate'))

    def test_browserlayer(self):
        """Test that IEcityclicGoogleTranslateLayer is registered."""
        from ecityclic.google_translate.interfaces import IEcityclicGoogleTranslateLayer
        from plone.browserlayer import utils
        self.assertIn(
            IEcityclicGoogleTranslateLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ECITYCLIC_GOOGLE_TRANSLATE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('ecityclic.google_translate')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if ecityclic.google_translate is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'ecityclic.google_translate'))

    def test_browserlayer_removed(self):
        """Test that IEcityclicGoogleTranslateLayer is removed."""
        from ecityclic.google_translate.interfaces import IEcityclicGoogleTranslateLayer
        from plone.browserlayer import utils
        self.assertNotIn(IEcityclicGoogleTranslateLayer, utils.registered_layers())
