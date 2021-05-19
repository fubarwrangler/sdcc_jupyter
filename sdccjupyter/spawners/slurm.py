import os
import re

from traitlets import Unicode
from tornado.log import app_log

from batchspawner import SlurmSpawner
from .pathoverride import PathOverrideMixin, override_path_slurm

from ..formspawners import FormMixin


class SDCCSlurmSpawner(FormMixin, PathOverrideMixin, SlurmSpawner):

    req_runtime = Unicode('30:00')
    req_gputype = Unicode('')
    req_scontainer = Unicode('')
    req_nbenv = Unicode('/u0b/software/jupyter/virtenvs/labenv3')
    startup_poll_interval = 1.5

    # Cancel here because it is called by our custom spawner
    batchspawner_singleuser_cmd = Unicode('')
    cmd = ['/u0b/software/jupyter/bin/basic_spawner.sh']


    @property
    def batch_script(self):
        self.log.info("My Actual Options: %s", self.user_options)
        base = [('partition', '{partition}'), ('account', '{account}'),
                ('time', '{runtime}')]
        if 'cpus' in self.user_options:
            base += [('cpus-per-task', '{nprocs}')]
        if 'memory' in self.user_options:
            base += [('mem', '{memory}G')]
        if 'ngpus' in self.user_options:
            base += [('gres', 'gpu:{ngpus}')]
        if 'gputype' in self.user_options:
            base += [('constraint', '{gputype}')]
        if 'qos' in self.user_options:
            base += [('qos', '{qos}')]

        extras = '\n'.join(['#SBATCH %s' % x for x in
                            self.user_options['extraopts'].split('\n')])

        prescript = '\n'.join('#SBATCH --{key}={value}'.format(
                                key=x[0], value=x[1]) for x in base)
        return '#!/bin/sh\n' + prescript + '''
#SBATCH --output={homedir}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --chdir={homedir}
#SBATCH --export={keepvars}
#SBATCH --get-user-env=L
''' + extras + '''
export NBENV="{nbenv}"
export SCONTAINER="{scontainer}"
unset XDG_RUNTIME_DIR
module load cuda/9.0
{cmd}
'''
