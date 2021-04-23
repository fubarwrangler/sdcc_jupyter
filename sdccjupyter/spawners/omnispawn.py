from .slurm import SDCCSlurmSpawner
from .condor import SDCCCondorSpawner

from ..formspawners import WrapFormSpawner, FormMixin


# Inherit from the class you want to use the form from...
class SDCCOmniSpawner(FormMixin, WrapFormSpawner):

    def set_class(self, data):
        app_log.debug("Choose class data: %s", data)
        if 'htc' in data:
            self.log.info("Choosing condor spawner... %s", data)
            x = SDCCCondorSpawner
            x.form_cls = self.form_cls
            return x
        else:
            self.log.info("Choosing SLURM spawner...")
            x = SDCCSlurmSpawner
            x.form_cls = self.form_cls
            return x
