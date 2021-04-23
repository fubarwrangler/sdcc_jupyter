import os
import re

from traitlets import Unicode
from tornado.log import app_log

from batchspawner import SlurmSpawner
from jupyterhub.spawner import LocalProcessSpawner

from ..formspawners import FormMixin, WrapFormSpawner


class SDCCSlurmSpawner(FormMixin, SlurmSpawner):

    req_jhubpath = Unicode('/u0b/software/jupyter/virtenvs/jhub_hostenv/bin')
    req_runtime = Unicode('30:00')
    req_gputype = Unicode('')
    req_scontainer = Unicode('')
    req_kpath = Unicode('/u0b/software/jupyter/')

    def check_path_override(self, account):
        kern_cfgfile = 'conf/kerneloverride.cfg'
        path = os.path.join(os.path.dirname(__file__), kern_cfgfile)
        with open(path) as fp:
            for regex, jp in (x.split() for x in fp):
                if re.match(regex, account):
                    self.log.info("Matched %s to %s, using jupyter_path = %s",
                                  account, regex, jp)
                    self.req_kpath = jp

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
        self.check_path_override(self.user_options.get('account'))
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
export PATH="{jhubpath}:$PATH"
export SCONTAINER="{scontainer}"
export JUPYTER_PATH="''' + self.req_kpath + '''"
unset XDG_RUNTIME_DIR
module load cuda/9.0
{cmd}
'''
