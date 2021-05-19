
import os
import re
import grp
import pwd

from tornado.log import app_log


def override(key, file):
    def parse_pathlist(paths):
        append = paths.startswith("+")
        paths = paths.lstrip("+")
        return append, paths.split(":")

    jupyter_path = list()

    with open(file) as fp:
        for regex, jp in (x.split() for x in fp if not x.startswith('#') and len(x) > 3):
            if re.match(regex, key):
                app_log.debug("Matched %s to %s, using jupyter_path = %s",
                              key, regex, jp)
                append, paths = parse_pathlist(jp)
                if append:
                    jupyter_path.extend(paths)
                else:
                    jupyter_path = paths

    return jupyter_path

def override_path_uid(username, cfgpath="../conf/pathoverride.cfg"):

    def primary_group(user):
        gid = pwd.getpwnam(user).pw_gid
        return grp.getgrgid(gid).gr_name

    group = primary_group(username)

    if not cfgpath.startswith('/'):
        cfgpath = os.path.join(os.path.dirname(__file__), cfgpath)

    return override(group, cfgpath)


def override_path_slurm(slurm_account, cfgpath='../conf/slurmoverride.cfg'):
    if not slurm_account:
        return []

    path = os.path.join(os.path.dirname(__file__), cfgpath)

    return override(slurm_account, path)

class PathOverrideMixin:
    def get_env(self):
        """Get the complete set of environment variables to be set in the spawned process """

        env = super().get_env()
        paths = override_path_uid(self.user.name)

        slurmaccount = self.user_options.get('account')
        if slurmaccount:
            paths = override_path_slurm(slurmaccount)
        env['JUPYTER_PATH'] = ":".join(paths)
        app_log.info("Path override: set JUPYTER_PATH to %s", env['JUPYTER_PATH'])
        return env
