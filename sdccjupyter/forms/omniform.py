import sqlite3
from jinja2 import Template
from tornado.log import app_log

from ..formspawners import ParamForm


class OmniForm(ParamForm):

    source = 'static/sdcc.html'
    db_path = '/var/tmp/slurm_accounts.db'

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
        days, hours, mins, sec = [0] * 4

        if len(s_m_hd) > 2:
            hd = s_m_hd.pop(0)
            if '-' in hd:
                days, hours = map(int, hd.split('-'))
            else:
                hours = int(hd)
        if len(s_m_hd) > 1:
            mins = int(s_m_hd.pop(0))
        return days * 24 * 60 + hours * 60 + mins

    def massage_options(self, formdata):
        data = super().massage_options(formdata)
        app_log.warning("massage_options(omniform) (%s): %s", self.spawner, data)
        intify = {'req_memory', 'req_nprocs', 'cpus', 'ram'}
        data = {k: int(v) if v in intify else v for k, v in data.items()}
        if data['req_gputype'] == "tesla":
            data['req_ngpus'] = '4'
        elif data['req_gputype'] == "pascal":
            data['req_ngpus'] = '2'
        else:
            data.pop('req_gputype')
            data['req_ngpus'] = '1'
        data['req_runtime'] = '%d:00' % int(data['req_runtime'])

        if data['spawntype'] == 'lbpool':
            data['req_options'] = 'Requirements = (IsJupyterSlot =?= True)'
        elif data['spawntype'] == 'htc':
            data['req_options'] = 'Requirements = (IsJupyterSlot =!= True)'
            data['req_nprocs'] = data['cpus']
            data['req_memory'] = data['ram']

        def no_req(k):
            return k[4:] if k.startswith('req_') else k

        return {no_req(k): v for k, v in data.items()}

    def generate(self):
        db = sqlite3.connect(self.db_path)
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

        return Template(super().generate()).render(**vars)