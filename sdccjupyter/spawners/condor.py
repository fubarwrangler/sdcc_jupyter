# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from traitlets import Unicode

from batchspawner import CondorSpawner

from ..formspawners import FormMixin


class SDCCCondorSpawner(FormMixin, CondorSpawner):

    # Maybe allow singularity-image selection logic some day too?
    req_scontainer = Unicode('')
    startup_poll_interval = 1.5

    # Cancel here because it is called by our custom spawner
    batchspawner_singleuser_cmd = Unicode('')

    cmd = ['/cvmfs/sdcc.bnl.gov/jupyter/bin/basic_spawner.sh']

    @property
    def batch_script(self):
        return '''
Executable = /bin/sh
Arguments = \"-c 'PATH=$NBENV/bin:$PATH {cmd}'\"
Remote_Initialdir = {homedir}
Output = {homedir}/.jupyterhub.$(clusterid).condor.out
Error = {homedir}/.jupyterhub.$(clusterid).condor.err
ShouldTransferFiles = False
GetEnv = True
PeriodicRemove = (JobStatus == 1 && NumJobStarts > 1) || JobStatus == 5
Queue
'''
