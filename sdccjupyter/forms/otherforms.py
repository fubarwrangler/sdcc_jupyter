from jinja2 import Template
from tornado.log import app_log

from .formspawners import ParamForm

import sqlite3

__all__ = ['CFNForm', 'NSLSForm', 'KNLForm', 'SDCCForm']


class CFNForm(ParamForm):

    source = 'static/cfn.html'

    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        intify = {'req_memory', 'req_nprocs'}
        data = {k: int(v) if v in intify else v for k, v in data.items()}
        data['req_runtime'] = '%d:00' % int(data['req_runtime'])
        return data

    def generate(self):
        app_log.info("Generating form from: %s", self)
        return Template(super().generate()).render()


class NSLSForm(ParamForm):
    source = 'static/nsls.html'

    def generate(self):
        app_log.info("Generating form from: %s", self)
        return Template(super().generate()).render()


class KNLForm(ParamForm):

    source = 'static/knl.html'

    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        data['req_runtime'] = '%d:00' % int(data['req_runtime'])
        return data

    def generate(self):
        app_log.info("Generating form from: %s", self)
        return Template(super().generate()).render()


class SDCCForm(ParamForm):

    source = 'static/sdcc.html'

    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        data['req_runtime'] = '%d:00' % int(data['req_runtime'])
        return data

    def generate(self):
        app_log.info("Generating form from: %s", self)
        return Template(super().generate()).render()
