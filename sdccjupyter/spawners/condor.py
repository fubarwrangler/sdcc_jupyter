# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from traitlets import Unicode

from batchspawner import CondorSpawner
from .pathoverride import PathOverrideMixin

from ..formspawners import FormMixin


class SDCCCondorSpawner(FormMixin, PathOverrideMixin, CondorSpawner):

    # Maybe allow singularity-image selection logic some day too?
    req_scontainer = Unicode('')

    req_nbenv = Unicode('/cvmfs/sdcc.bnl.gov/jupyter/virtualenv/labenv')

    startup_poll_interval = 1.5

    # Cancel here because it is called by our custom spawner
    batchspawner_singleuser_cmd = Unicode('')

    cmd = ['/cvmfs/sdcc.bnl.gov/jupyter/bin/basic_spawner.sh']

    @property
    def batch_script(self):
        self.log.info("HTCondor Actual Options: %s", self.user_options)
        return '''
Executable = /bin/sh
Arguments = \"-c 'PATH=$NBENV/bin:$PATH exec {cmd}'\"
Remote_Initialdir = {homedir}
Output = {homedir}/.jupyterhub.condor.out
Error = {homedir}/.jupyterhub.condor.err
ShouldTransferFiles = False
Environment = NBENV={nbenv}
GetEnv = True
Request_Memory = {memory}
Request_Cpus = {nprocs}
PeriodicRemove = (JobStatus == 1 && NumJobStarts > 1) || JobStatus == 5
{options}
Queue
'''
