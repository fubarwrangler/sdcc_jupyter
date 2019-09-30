# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from traitlets import Unicode
from tornado.log import app_log

from batchspawner import CondorSpawner

from .formspawners import FormMixin  # , WrapFormSpawner


class NSLSSpawner(FormMixin, CondorSpawner):

    # Maybe allow singularity-image selection logic some day too?
    req_scontainer = Unicode('')
    req_nbenv = Unicode('')

    @property
    def batch_script(self):
        self.req_nbenv = self.user_options['req_nbenv']
        self.log.info("My Actual Options: %s", self.user_options)
        self.log.info("My traits: %s", self.trait_names())
        self.log.info("My property env: %s", self.req_nbenv)
        return '''
Executable = /bin/sh
Arguments = \"-c 'PATH={nbenv}:$PATH exec {cmd}'\"
Remote_Initialdir = {homedir}
Output = {homedir}/.jupyterhub.$(clusterid).condor.out
Error = {homedir}/.jupyterhub.$(clusterid).condor.err
ShouldTransferFiles = False
GetEnv = True
PeriodicRemove = (JobStatus == 1 && NumJobStarts > 1)
Queue
'''

# This would be used as the spawner if the form had an option that would allow
# selecting of different actual spawners base on the options passed...
# vvvvv
#class NSLSSpawner(WrapFormSpawner, NSLSCondorSpawn):
#
#    def set_class(self, data):
#        app_log.debug("Choose class data: %s", data)
#        if 'local' in data:
#            self.log.info("Choosing local spawner... %s", data)
#            return LocalProcessSpawner
#        else:
#            self.log.info("Choosing SLURM spawner...")
#            x = SDCCSlurmSpawner
#            x.form_cls = self.form_cls
#            return x
