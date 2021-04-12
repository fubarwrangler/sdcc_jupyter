#!/bin/bash

set -x


export PATH="/u0b/software/jupyter/virtenvs/nbenv/bin:/usr/bin:/usr/sbin"

export TZ="US/Eastern"

export NSLS2_CATALOGS_PASSWORD_AMX=xxx
# ...


if [[ -x "$HOME/.jupyter_override" ]]; then
        run="$HOME/.jupyter_override"
elif [[ -n "$JHUBPAYLOAD" ]]; then
        run="$JHUBPAYLOAD"
else
        run="jupyterhub-singleuser"
fi

#echo "Will run: $run"
if [[ -z "$SCONTAINER" ]]; then
        exec "$run" "$@" --NotebookApp.default_url=/lab
else
        CONTAINER_FILENAME=$(basename $SCONTAINER)  # Strip path off.
        # REPO_DIRECTORY=$(echo "$CONTAINER_FILENAME" | cut -f 1 -d '.')  # Strip .sif off.
        REPO_DIRECTORY=$CONTAINER_FILENAME

        unset XDG_RUNTIME_DIR
        JUPYTER_RUNTIME_DIR=/tmp/jupyter-$USER-runtime
        JUPYTER_DATA_DIR=$HOME/.local/share/jupyter
        JUPYTER_CONFIG_DIR=$HOME/.jupyter
        # Make isolated workspaces per repo.
        JUPYTERLAB_WORKSPACES_DIR=$JUPYTER_CONFIG_DIR/lab/workspaces/$REPO_DIRECTORY
        # Copy files.
        # This works but is slow.
        # singularity exec $SCONTAINER python3 -c "import shutil; shutil.copytree('/home/jovyan', '$HOME/$REPO_DIRECTORY')"
        mkdir -p $HOME/$REPO_DIRECTORY
        # Launch container.
        # Server root will be $HOME; initial working directory will be $HOME/$REPO_DIRECTORY.
        exec env SINGULARITYENV_SINGULAIRTY_USER=$USER SINGULARITYENV_REPO_DIR=$REPO_DIRECTORY env SINGULARITYENV_JUPYTER_DATA_DIR=$JUPYTER_DATA_DIR env SINGULARITYENV_JUPYTER_RUNTIME_DIR=$JUPYTER_RUNTIME_DIR env SINGULARITYENV_JUPYTER_CONFIG_DIR=$JUPYTER_CONFIG_DIR singularity exec --nv --writable-tmpfs -B /direct/u0b/software:/direct/u0b/software -B /u0b/software:/u0b/software -B /nsls2:/nsls2 $SCONTAINER $run --notebook-dir=$HOME --NotebookApp.default_url=/lab/workspaces/lab/tree/$REPO_DIRECTORY?reset "$@"
fi
