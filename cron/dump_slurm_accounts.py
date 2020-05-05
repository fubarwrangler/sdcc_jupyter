#!/usr/bin/env python
# Run this script as a cronjob every night or so to dump to a local SQLite DB
# the slurm user->account->qos->partition mapping for spawner form

import subprocess
import sqlite3
import sys

sacct_cmd = ['sacctmgr', 'show', 'associations',
             '-n', '-P', 'format=User,Qos,Account']

sacct_qos_cmd = ['sacctmgr', 'show', 'qos', '-n', '-P', 'format=Name,MaxWall']
# user -> account -> qos
users = {}

DBFILE = '/var/tmp/slurm_accounts.db'

kw = {} if sys.version_info[0] < 3 else {'encoding': 'utf8'}

for line in subprocess.check_output(sacct_cmd, **kw).split('\n'):
    # Skip lines that aren't regular users
    if line.startswith("|") or len(line) == 0:
        continue
    user, qoslist, acct = line.split("|")
    qos = set(qoslist.split(','))
    if user in users:
        users[user][acct] = qos
    else:
        users[user] = {acct: qos}

# Partition -> [qos-list]
partitions = dict()
for pair in (x.strip().split() for x in open('/etc/slurm/slurm.conf')):
    if len(pair) == 0 or not pair[0].startswith("PartitionName="):
        continue
    name = pair.pop(0)[14:]
    qoslist = next(x[9:] for x in pair if x.startswith('AllowQOS'))

    partitions[name] = qoslist.split(',')

qos_part_time = dict()
for line in subprocess.check_output(sacct_qos_cmd, **kw).split('\n'):
    if len(line) == 0 or line.startswith("|"):
        continue
    name, time = line.split("|")
    if name.startswith("part_"):
        qos_part_time[name[5:]] = time

db = sqlite3.connect(DBFILE)
cur = db.cursor()
cur.executescript("""
CREATE TABLE IF NOT EXISTS users (
    username text,
    account text,
    qos text,
    PRIMARY KEY (username, account, qos)
);
CREATE TABLE IF NOT EXISTS partitions (
    partition text,
    time text,
    qos text
);
CREATE INDEX IF NOT EXISTS idx_part_qos ON partitions (qos);
CREATE INDEX IF NOT EXISTS idx_user_qos ON users (qos);
""")
cur.execute('DELETE FROM users')
cur.executemany('INSERT INTO users VALUES (?,?,?)',
                ((user, acct, qos) for user in users
                    for acct in users[user]
                    for qos in users[user][acct]))
cur.execute('DELETE FROM partitions')
cur.executemany('INSERT INTO partitions VALUES (?,?,?)',
                ((p,qos_part_time[p], q) for p in partitions for q in partitions[p]))
db.commit()
db.close()
