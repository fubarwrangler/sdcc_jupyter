# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from traitlets import Unicode
# from tornado.log import app_log

from batchspawner import CondorSpawner

from .formspawners import FormMixin  # , WrapFormSpawner


class NSLSSpawner(FormMixin, CondorSpawner):

    # Maybe allow singularity-image selection logic some day too?
    req_scontainer = Unicode('')

    @property
    def batch_script(self):
        return '''
Executable = /bin/sh
Arguments = \"-c 'PATH={nbenv}/bin:$PATH exec {cmd}'\"
Remote_Initialdir = {homedir}
Output = {homedir}/.jupyterhub.$(clusterid).condor.out
Error = {homedir}/.jupyterhub.$(clusterid).condor.err
ShouldTransferFiles = False
GetEnv = True
PeriodicRemove = (JobStatus == 1 && NumJobStarts > 1)
Queue
'''
