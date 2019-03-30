#!/usr/bin/env python

import subprocess, sys

# sacct_cmd = ['sacctmgr', 'show', 'associations', '-n', '-P', 'format=User,Qos,Account']
sacct_cmd = ['cat', '/home/willsk/output.txt']

# user -> account -> qos
users = {}

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
for pair in (x.strip().split() for x in open('slurm.conf')):
    if len(pair) == 0 or not pair[0].startswith("PartitionName="):
        continue
    name = pair.pop(0)[14:]
    time = next(x[8:] for x in pair if x.startswith('MaxTime'))
    qoslist = next(x[9:] for x in pair if x.startswith('AllowQOS'))

    partitions[name] = (time, qoslist.split(','))
