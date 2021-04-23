from jupyterhub.spawner import LocalProcessSpawner
from .pathoverride import PathOverrideMixin


class LocalPathOverrideSpawner(LocalProcessSpawner, PathOverrideMixin):
    pass
