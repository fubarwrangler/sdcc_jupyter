from tornado.log import app_log

from .slurm import SDCCSlurmSpawner
from .condor import SDCCCondorSpawner
from .local import LocalPathOverrideSpawner

from ..formspawners import WrapFormSpawner, FormMixin

from traitlets import Type
from jupyterhub.spawner import Spawner



# Inherit from the class you want to use the form from...
class SDCCOmniSpawner(WrapFormSpawner):

    child_class = Type(Spawner,
                       config=True,
                       help="""The class to wrap for spawning single-user servers.
                               Should be a subclass of Spawner.
                            """
                       )

    def set_class(self, data):
        self.log.info("set_class: data=%s", data)

        if data.get('spawntype') in ['htc', 'lbpool']:
            self.log.info("Choosing condor spawner... %s", data)
            self.child_class = SDCCCondorSpawner
        else:
            self.log.info("Choosing SLURM spawner...")
            self.child_class = SDCCSlurmSpawner

        self.child_config = data
        self.child_class.user_options = data
