from jupyterhub.spawner import LocalProcessSpawner
from .sdccslurm import SlurmSpawner
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
        return formdata


class ParamFormText(ParamForm):

    def generate(self):
        return self.source

# Foo
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


class FormLocalSpawner(FormMixin, LocalProcessSpawner):
    pass


class FormSlurmSpawner(FormMixin, SlurmSpawner):
    # req_partition = Unicode('', )
    pass
