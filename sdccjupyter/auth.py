from jhub_remote_user_authenticator.remote_user_auth import RemoteUserAuthenticator
from jupyterhub.handlers import BaseHandler
from traitlets import Unicode


class SDCCLogout(BaseHandler):
    """ Log a user out by clearing their login cookie. Very similar to basic
        one except we redirect to the root URL and clear our ROUTE cookie if
        we are a load-balanced backend.
    """

    async def get(self):
        user = await self.get_current_user()
        if user:
            self.log.info("User logged out: %s", user.name)
            self.clear_login_cookie()
            if self.get_cookie('ROUTEID'):
                self.clear_cookie('ROUTEID')
            self.statsd.incr('logout')
        self.log.debug("Logout complete, redirect to: %s",
                       self.authenticator.logout_destination)
        self.redirect(self.authenticator.logout_destination, permanent=False)


class SDCCAuthenticator(RemoteUserAuthenticator):
    logout_destination = Unicode('/', help="URL to hit once you log out").tag(config=True)

    def get_handlers(self, app):
        return super().get_handlers(app) + [
            (r'/logout', SDCCLogout),
        ]
