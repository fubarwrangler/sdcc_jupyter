from traitlets import Unicode
from tornado.log import app_log

from batchspawner import SlurmSpawner
from jupyterhub.spawner import LocalProcessSpawner

from .formspawners import FormMixin, WrapFormSpawner


class SDCCSlurmSpawner(FormMixin, SlurmSpawner):

    req_jhubpath = Unicode('/u0b/software/jupyter/virtenvs/jhub_hostenv/bin')
    req_runtime = Unicode('30:00')
    req_gputype = Unicode('')
    req_scontainer = Unicode('')

    @property
    def batch_script(self):
        # self.log.info("My form Options: %s", self.user_)
        self.log.info("My Actual Options: %s", self.user_options)
        base = [('partition', '{partition}'), ('account', '{account}'),
                ('time', '{runtime}')]
        if 'req_cpus' in self.user_options:
            base += [('cpus-per-task', '{nprocs}')]
        if 'req_memory' in self.user_options:
            base += [('mem', '{memory}G')]
        if 'req_ngpus' in self.user_options:
            base += [('gres', 'gpu:{ngpus}')]
        if 'req_gputype' in self.user_options:
            base += [('constraint', '{gputype}')]
        if 'req_qos' in self.user_options:
            base += [('qos', '{qos}')]
        prescript = '\n'.join('#SBATCH --{key}={value}'.format(
                                key=x[0], value=x[1]) for x in base)
        return '#!/bin/sh\n' + prescript + '''
#SBATCH --output={homedir}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --chdir={homedir}
#SBATCH --export={keepvars}
#SBATCH --get-user-env=L
#SBATCH {options}
export PATH="{jhubpath}:$PATH"
export SCONTAINER="{scontainer}"
unset XDG_RUNTIME_DIR
{cmd}
'''


# Inherit from the class you want to use the form from...
class SDCCSpawn(WrapFormSpawner, SDCCSlurmSpawner):

    def set_class(self, data):
        app_log.debug("Choose class data: %s", data)
        if 'local' in data:
            self.log.info("Choosing local spawner... %s", data)
            return LocalProcessSpawner
        else:
            self.log.info("Choosing SLURM spawner...")
            x = SDCCSlurmSpawner
            x.form_cls = self.form_cls
            return x
