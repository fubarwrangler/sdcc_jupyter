from traitlets import Unicode

from batchspawner import SlurmSpawner
from jupyterhub.spawner import LocalProcessSpawner

from .formspawners import FormMixin, WrapFormSpawner
from .forms import CFNForm, ICForm


class SDCCSlurmSpawner(FormMixin, SlurmSpawner):

    req_jhubpath = Unicode('/u0b/software/jupyter/virtenvs/jhub_hostenv/bin')
    req_runtime = Unicode('30:00')
    req_scontainer = Unicode('')
    cmd = ['/u0b/software/images/container_run.sh']

    @property
    def batch_script(self):
        self.log.info("My script Options: %s", self.formdata)
        base = [('partition', '{partition}'), ('account', '{account}'),
                ('time', '{runtime}')]
        if 'req_cpus' in self.formdata:
            base += [('cpus-per-task', '{nprocs}')]
        if 'req_memory' in self.formdata:
            base += [('mem', '{memory}G')]
        if 'req_ngpus' in self.formdata:
            base += [('gres', 'gpu:{ngpus}')]
        prescript = '\n'.join('#SBATCH --{key}={value}'.format(
                                key=x[0], value=x[1]) for x in base)
        return '#!/bin/sh\n' + prescript + '''
#SBATCH --output={homedir}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --workdir={homedir}
#SBATCH --export={keepvars}
#SBATCH --get-user-env=L
#SBATCH {options}
export PATH="{jhubpath}:$PATH"
export SCONTAINER="{scontainer}"
unset XDG_RUNTIME_DIR
{cmd}
'''


# Inherit from the class you want to use the form from...
class CFNSpawn(WrapFormSpawner, SDCCSlurmSpawner):

    form_cls = ICForm

    def set_class(self, data):
        if 'local' in data:
            self.log.info("Choosing local spawner... %s", data)
            return LocalProcessSpawner
        else:
            self.log.info("Choosing SLURM spawner...")
            x = SDCCSlurmSpawner
            x.form_cls = self.form_cls
            return x
