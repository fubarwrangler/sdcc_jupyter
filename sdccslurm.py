from batchspawner import SlurmSpawner as origSlurmSpawner
from traitlets import Unicode


class SlurmSpawner(origSlurmSpawner):
    req_jhubpath = Unicode('/u0b/software/anaconda3/bin')
    req_runtime = Unicode('30:00')
    batch_script = '''#!/bin/sh
#SBATCH --partition={partition}
#SBATCH --time={runtime}
#SBATCH --output={homedir}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --workdir={homedir}
#SBATCH --gres=gpu:{ngpus}
#SBATCH --export={keepvars}
#SBATCH --get-user-env=L
#SBATCH --account={account}
#SBATCH {options}
export PATH="{jhubpath}:$PATH"
unset XDG_RUNTIME_DIR
{cmd}
'''
