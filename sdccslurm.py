from batchspawner import SlurmSpawner as origSlurmSpawner


class SlurmSpawner(origSlurmSpawner):
    req_partition = 'usatlas'
    req_jhubpath = '/u0b/software/anaconda3/bin'
    batch_script = '''#!/bin/sh
#SBATCH --partition={partition}
#SBATCH --time={runtime}
#SBATCH --output={homedir}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --workdir={homedir}
#SBATCH --export={keepvars}
#SBATCH --get-user-env=L
#SBATCH --account={account}
#SBATCH {options}
export PATH="{jhubpath}:$PATH"
unset XDG_RUNTIME_DIR
{cmd}
'''
