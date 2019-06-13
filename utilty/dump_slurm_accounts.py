#!/usr/bin/env python2
# Run this script as a cronjob every night or so to dump to a local SQLite DB
# the slurm user->account->qos->partition mapping for spawner form

import subprocess
import sqlite3

sacct_cmd = ['sacctmgr', 'show', 'associations',
             '-n', '-P', 'format=User,Qos,Account']
# user -> account -> qos
users = {}

DBFILE = '/var/tmp/slurm_accounts.db'

for line in subprocess.check_output(sacct_cmd).split('\n'):
    # Skip lines that aren't regular users
    if line.startswith("|") or len(line) == 0:
        continue
    user, qoslist, acct = line.split("|")
    qos = set(qoslist.split(','))
    if user in users:
        users[user][acct] = qos
    else:
        users[user] = {acct: qos}

# Partition -> (max-time, [qos-list])
partitions = dict()
for pair in (x.strip().split() for x in open('/etc/slurm/slurm.conf')):
    if len(pair) == 0 or not pair[0].startswith("PartitionName="):
        continue
    name = pair.pop(0)[14:]
    time = next(x[8:] for x in pair if x.startswith('MaxTime'))
    qoslist = next(x[9:] for x in pair if x.startswith('AllowQOS'))

    partitions[name] = (time, qoslist.split(','))

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
                ((p, partitions[p][0], q) for p in partitions for q in partitions[p][1]))
db.commit()
db.close()
