from jupyterhub.spawner import LocalProcessSpawner
from .sdccslurm import SlurmSpawner
from wrapspawner import WrapSpawner
from traitlets import Unicode, Type, Instance

import os

from traitlets.config.configurable import HasTraits


class ParamForm(HasTraits):
    source = Unicode()

    def __init__(self, source):
        self.source = source

    def generate(self):
        path = os.path.join(os.path.dirname(__file__), self.source)
        with open(path) as f:
            return f.read()

    def massage_options(self, formdata):
        return {k: v[0] for k, v in formdata.items()}


class ParamFormText(ParamForm):

    def generate(self):
        return self.source


class SlurmForm(ParamForm):
    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        intify = {'req_memory', 'req_ngpus'}
        data = {k: int(v) if v in intify else v for k, v in data.items()}
        partition, account = data['req_partition'].split('+')
        data['req_partition'] = partition
        data['req_account'] = account
        return data


class FormMixin(HasTraits):

    form_inst = Instance(ParamForm, help="Instance fo the form class to use"
                         ).tag(config=True)

    @staticmethod
    def options_form(self):
        self.log.debug(self.form_inst)
        return self.form_inst.generate()

    def options_from_form(self, formdata):
        self.log.warning("GENREATING FORM: %s", formdata)
        return self.form_inst.massage_options(formdata)


class WrapFormSpawner(FormMixin, WrapSpawner):
    def options_from_form(self, formdata):
        self.child_class = self.set_class(formdata)
        self.child_config = self.form_inst.massage_options(formdata)
        self.log.debug("My child config: %s", self.child_config)
        return {}

    def set_class(self, data):
        raise NotImplementedError('Must implement in subclass')


class FormLocalSpawner(FormMixin, LocalProcessSpawner):
    pass


class FormSlurmSpawner(FormMixin, SlurmSpawner):
    # req_partition = Unicode('', )
    def options_from_form(self, formdata):
        self.log.info("SLURM: config: %s", formdata)
        return formdata


class ChooseSpawner(WrapFormSpawner):
    def set_class(self, data):
        if 'local' in data:
            self.log.info("Choosing local spawner...")
            return LocalProcessSpawner
        else:
            self.log.info("Choosing SLURM spawner...")
            return FormSlurmSpawner
