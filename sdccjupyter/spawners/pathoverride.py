
import os
import re
import grp
import pwd

from tornado.log import app_log


def primary_group(user):
    gid = pwd.getpwnam(user).pw_gid
    return grp.getgrgid(gid).gr_name


def override_path(username, cfgpath="conf/pathoverride.cfg"):

    def parse_pathlist(paths):
        append = paths.startswith("+")
        paths = paths.lstrip("+")
        return append, paths.split(":")

    group = primary_group(username)

    if not cfgpath.startswith('/'):
        cfgpath = os.path.join(os.path.dirname(__file__), cfgpath)
    jupyter_path = list()

    with open(cfgpath) as fp:
        for regex, jp in (x.split() for x in fp if not x.startswith('#') and len(x) > 3):
            if re.match(regex, group):
                append, paths = parse_pathlist(jp)
                if append:
                    jupyter_path.extend(paths)
                else:
                    jupyter_path = paths
    return jupyter_path


class PathOverrideMixin:
    def get_env(self):
        """Get the complete set of environment variables to be set in the spawned process """

        env = super().get_env()
        env['JUPYTER_PATH'] = ":".join(override_path(self.user.name))
        app_log.info("Path override: set JUPYTER_PATH to %s", env['JUPYTER_PATH'])
        return env
