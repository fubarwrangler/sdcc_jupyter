from jupyterhub.spawner import LocalProcessSpawner
from .pathoverride import PathOverrideMixin


class LocalOverrideSpawner(LocalProcessSpawner, PathOverrideMixin):
    pass
