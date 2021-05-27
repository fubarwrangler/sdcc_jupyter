
import os

from tornado.log import app_log
from ruamel.yaml import YAML
from .utils import get_all_groupnames


def get_lab_locations(user, cfg="../conf/lab-locations.yml"):
    cfgpath = os.path.join(os.path.dirname(__file__), cfg)

    yaml = YAML(typ='safe')
    with open(cfgpath) as fp:
        data = yaml.load(fp)
    locations = data['locations']
    group_map = data['groups']

    available_labs = set()

    for group in get_all_groupnames(user):
        if group in group_map:
            for lab in group_map[group]:
                available_labs.add(lab)

    return [(x, locations[x]) for x in group_map['all'] + list(available_labs)]
