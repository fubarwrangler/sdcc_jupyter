from traitlets import Unicode
from jinja2 import Template

from batchspawner import SlurmSpawner
from jupyterhub.spawner import LocalProcessSpawner

from .formspawners import ParamForm, FormMixin, WrapFormSpawner


class SDCCSlurmSpawner(SlurmSpawner):
    req_jhubpath = Unicode('/u0b/software/anaconda3/bin')
    req_runtime = Unicode('30:00')
    batch_script = '''#!/bin/sh
#SBATCH --partition={partition}
#SBATCH --time={runtime}
#SBATCH --output={homedir}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --workdir={homedir}
#SBATCH --gres=gpu:{ngpus}
#SBATCH --export={keepvars}
#SBATCH --get-user-env=L
#SBATCH --account={account}
#SBATCH {options}
export PATH="{jhubpath}:$PATH"
unset XDG_RUNTIME_DIR
{cmd}
'''


class SlurmForm(ParamForm):

    source = 'static/ic.html'

    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        intify = {'req_memory', 'req_ngpus'}
        data = {k: int(v) if v in intify else v for k, v in data.items()}
        partition, account = data['req_partition'].split('+')
        data['req_partition'] = partition
        data['req_account'] = account
        data['req_runtime'] = '%d:00' % int(data['req_runtime'])
        return data

    def generate(self):
        vars = {}
        return Template(super().generate()).render(**vars)


class FormSlurmSpawner(FormMixin, SDCCSlurmSpawner):

    form_cls = SlurmForm

    def options_from_form(self, formdata):
        self.log.info("SLURM: config: %s", formdata)
        return formdata


class ChooseSlurmSpawner(WrapFormSpawner):

    form_cls = SlurmForm

    def set_class(self, data):
        if 'local' in data:
            self.log.info("Choosing local spawner... %s", data)
            return LocalProcessSpawner
        else:
            self.log.info("Choosing SLURM spawner...")
            return FormSlurmSpawner
