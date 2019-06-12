from jinja2 import Template
from tornado.log import app_log

from .formspawners import ParamForm

import sqlite3


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


class ICForm(ParamForm):

    source = 'static/ic.html'

    # # Category: list[ (Name, path), (name2, path2)... ]
    # containers = {
    #     'Native': [('Native', '')],
    #     'Generic': [
    #         ('SL7.3', '/u0b/software/images/generic-SL7.simg'),
    #         ('SL6.4', '/u0b/software/images/generic-SL6.simg'),
    #     ],
    #     'USATLAS': [
    #         ('Doug\'s Container', '/u0b/software/images/generic-SL7.simg'),
    #     ],
    # }
    #
    # # Partition+account, display-name, container-image-path
    # partitions = (
    #     ["usatlas+pq302951", 'USAtlas', '/u0b/software/images/generic-SL7.simg'],
    #     ['debug+default', 'Debug', ''],
    # )

    query = '''
    SELECT DISTINCT partitions.partition, qos.*, time FROM users
        JOIN qos ON qos.account=users.account
        JOIN partitions ON qos.qos=partitions.qos
    WHERE username=?
    ORDER BY partition, partitions.qos, qos.account;
    '''

    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        intify = {'req_memory', 'req_ngpus'}
        data = {k: int(v) if v in intify else v for k, v in data.items()}
        app_log.debug(data)
        partition, account = data['req_partition'].split('+')
        data['req_partition'] = partition
        data['req_account'] = account
        data['req_runtime'] = '%d:00' % int(data['req_runtime'])
        return data

    def generate(self):
        db = sqlite3.connect('/var/tmp/slurm_accounts.db')
        cur = db.cursor()
        cur.execute(self.query, [self.spawner.user.name])

        # Tuples of : (partition, account, qos, timelimit), ...
        slurm_params = cur.fetchall()
        vars = {
            'partitions': {(x[0], x[3]) for x in slurm_params},
            'accounts': {x[1] for x in slurm_params},
            'qos': {x[2] for x in slurm_params},
            'slurm': slurm_params,
        }
        db.close()
        app_log.info(vars)

        return Template(super().generate()).render(**vars)
