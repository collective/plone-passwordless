from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from operator import itemgetter
from .interfaces import IPasswordlessPlugin
from plone import api
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.interfaces.capabilities import IDeleteCapability
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PluggableAuthService.events import PrincipalCreated
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.interfaces.authservice import _noroles
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.event import notify
from zope.interface import implementer

import logging
import os


logger = logging.getLogger(__name__)
tpl_dir = os.path.join(os.path.dirname(__file__), "browser")

_marker = {}

ANNOTATION_ID = '_plone_passwordless'


def manage_addPasswordlessPlugin(context, id, title="", RESPONSE=None, **kw):
    """Create an instance of a Passwordless Plugin."""
    plugin = PasswordlessPlugin(id, title, **kw)
    context._setObject(plugin.getId(), plugin)
    if RESPONSE is not None:
        RESPONSE.redirect("manage_workspace")


manage_addPasswordlessPluginForm = PageTemplateFile(
    os.path.join(tpl_dir, "add_plugin.pt"),
    globals(),
    __name__="addPasswordlessPlugin",
)


@implementer(
    IPasswordlessPlugin,
    pas_interfaces.IAuthenticationPlugin,
    pas_interfaces.IRolesPlugin,
    pas_interfaces.IUserEnumerationPlugin,
)
class PasswordlessPlugin(BasePlugin):
    """Passwordless PAS Plugin"""

    security = ClassSecurityInfo()
    meta_type = "Passwordless Plugin"
    BasePlugin.manage_options

    # Tell PAS not to swallow our exceptions
    _dont_swallow_my_exceptions = True

    def __init__(self, id, title=None, **kw):
        self._setId(id)
        self.title = title
        self.plugin_caching = True
        self._init_trees()

    def _init_trees(self):
        # (provider_name, provider_userid) -> userid
        tree = getattr(self, ANNOTATION_ID, None)
        if tree is None:
            setattr(self, ANNOTATION_ID, OOBTree())

    @security.public
    def authenticateCredentials(self, credentials):
        """credentials -> (userid, login)

        - 'credentials' will be a mapping, as returned by IExtractionPlugin.
        - Return a  tuple consisting of user ID (which may be different
          from the login name) and login
        - If the credentials cannot be authenticated, return None.
        """

        login = credentials.get("login", None)
        password = credentials.get("password", None)
        if login == "aj":
            print("authenticated")
            return "aj", "aj"

        return None

    @security.public
    def getRolesForPrincipal(self, principal, request=None):
        """ All users authenticated through this plugin get fixed roles """

        if principal == "aj":
            print("inside roles")
            return ("Member", "Authenticated")
        return ()


    @security.public
    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):

        print("enumerateUsers")
        result = [dict(login="aj", id="aj", plugin_id="passwordless")]
        return result

InitializeClass(PasswordlessPlugin)
