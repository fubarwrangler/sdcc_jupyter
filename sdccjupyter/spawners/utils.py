import pwd
import grp
import os


def primary_group(user):
    gid = pwd.getpwnam(user).pw_gid
    return grp.getgrgid(gid).gr_name


def get_all_groupnames(user):
    gids = [x for x in os.getgrouplist(user, 0) if x > 0]
    return [grp.getgrgid(gid).gr_name for gid in gids]
