#!/bin/bash

if [[ -x "$HOME/.jupyter_override" ]]; then
	run="$HOME/.jupyter_override"
elif [[ -n "$JHUBPAYLOAD" ]]; then
        run="$JHUBPAYLOAD"
else
	run="jupyterhub-singleuser"
fi

#echo "Will run: $run"

if [[ -z "$SCONTAINER" ]]; then
	exec "$run" "$@"
else
	export SINGULARITYENV_PATH=$PATH
	unset XDG_RUNTIME_DIR
	exec singularity exec --nv -B /direct/u0b/software:/direct/u0b/software -B /u0b/software:/u0b/software $SCONTAINER $run "$@"
fi
