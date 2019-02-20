import os
from jupyterhub.spawner import LocalProcessSpawner
from traitlets import Unicode, Type

from traitlets.config.configurable import HasTraits


class ParamForm(HasTraits):
    text = Unicode()
    src = Unicode('default.html')

    def generate(self):
        if self.text:
            return self.text
        else:
            with open(self.src) as f:
                return f.read()

    def massage_options(self, formdata):
        return formdata


class DemoFormSpawner(LocalProcessSpawner):

    form_cls = ParamForm()

    @staticmethod
    def options_form(self):
        self.log.debug(self.form_cls)
        return self.form_cls.generate()

    def options_from_form(self, formdata):
        self.log.debug(formdata)
        return self.form_cls.massage_options(formdata)
