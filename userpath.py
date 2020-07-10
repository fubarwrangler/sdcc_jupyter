import os
import re
import grp
import pwd


def primary_group(user):
    gid = pwd.getpwnam(user).pw_gid
    return grp.getgrgid(gid).gr_name


def parse_pathlist(paths):
    append = paths.startswith("+")
    paths = paths.lstrip("+")
    return append, paths.split(":")


def override_path(username):
    cfg = 'conf/pathoverride.cfg'
    group = primary_group(username)

    jupyter_path = list()
    path = os.path.join(os.path.dirname(__file__), cfg)
    with open(path) as fp:
        for regex, jp in (x.split() for x in fp if not x.startswith('#')):
            if re.match(regex, group):
                append, paths = parse_pathlist(jp)
                if append:
                    jupyter_path.extend(paths)
                else:
                    jupyter_path = paths
    return jupyter_path
