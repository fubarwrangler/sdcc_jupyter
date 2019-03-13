from jhub_remote_user_authenticator.remote_user_auth import RemoteUserAuthenticator
from jupyterhub.handlers import BaseHandler
from traitlets import Unicode


class SDCCLogout(BaseHandler):
    """ Log a user out by clearing their login cookie. Very similar to basic
        one except we redirect to the root URL
    """

    def get(self):
        user = self.get_current_user()
        if user:
            self.log.info("User logged out: %s", user.name)
            self.clear_login_cookie()
            self.statsd.incr('logout')
        self.redirect(self.authenticator.logout_destination, permanent=False)


class SDCCAuthenticator(RemoteUserAuthenticator):
    logout_destination = Unicode('/', help="URL to hit once you log out")

    def get_handlers(self, app):
        return super().get_handlers(app) + [
            (r'/logout', SDCCLogout),
        ]
