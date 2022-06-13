# -*- coding: utf-8 -*-

from .interfaces import DEFAULT_ID
from .plugin import PasswordlessPlugin
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

TITLE = "Passwordless plugin (plone.passwordless)"


def _add_plugin(pas, pluginid=DEFAULT_ID):
    if pluginid in pas.objectIds():
        return TITLE + " already installed."
    if pluginid != DEFAULT_ID:
        return f"ID of plugin must be {DEFAULT_ID}"
    plugin = PasswordlessPlugin(pluginid, title=TITLE)
    pas._setObject(pluginid, plugin)
    plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
    for info in pas.plugins.listPluginTypeInfo():
        interface = info["interface"]
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface,
            [x[0] for x in pas.plugins.listPlugins(interface)[:-1]],
        )


def _remove_plugin(pas, pluginid=DEFAULT_ID):
    if pluginid in pas.objectIds():
        pas.manage_delObjects([pluginid])


def post_install(context):
    _add_plugin(context.aq_parent.acl_users)


def post_uninstall(context):
    _remove_plugin(context.aq_parent.acl_users)


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "plone.passwordless:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["plone.passwordless.upgrades"]
