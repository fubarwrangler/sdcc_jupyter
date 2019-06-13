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

    query = '''
    SELECT DISTINCT partitions.partition, users.account, users.qos, time FROM users
        JOIN partitions ON users.qos=partitions.qos
    WHERE username=?
    ORDER BY partition, partitions.qos, users.account;
    '''

    @staticmethod
    def slurm_time_to_min(timestr):
        # Strings look like '1-12:30:00' for 1 day 12 1/2 hours
        s_m_hd = timestr.split(':')
        days, hours, min, sec = [0] * 4

        if len(s_m_hd) > 2:
            hd = s_m_hd.pop(0)
            if '-' in hd:
                days, hours = map(int, hd.split('-'))
            else:
                hours = int(hd)
        if len(s_m_hd) > 1:
            min = int(s_m_hd.pop(0))
        return days * 24 * 60 + hours * 60 + min

    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        intify = {'req_memory', 'req_ngpus'}
        data = {k: int(v) if v in intify else v for k, v in data.items()}
        app_log.debug(data)
        data['req_runtime'] = '%d:00' % int(data['req_runtime'])
        return data

    def generate(self):
        db = sqlite3.connect('/var/tmp/slurm_accounts.db')
        cur = db.cursor()
        cur.execute(self.query, [self.spawner.user.name])

        # Tuples of : (partition, account, qos, timelimit), ...
        slurm_params = list()
        for row in map(list, cur.fetchall()):
            # Convert to minutes
            row[3] = self.slurm_time_to_min(row[3])
            row[3] -= row[3] % 30
            slurm_params.append(row)

        vars = {
            'partitions': list(sorted({(x[0], x[3]) for x in slurm_params})),
            'slurm': slurm_params,
        }
        db.close()
        app_log.info(vars)

        return Template(super().generate()).render(**vars)
