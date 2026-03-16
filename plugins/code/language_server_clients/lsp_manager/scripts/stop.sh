#!/bin/bash

. CONFIG.sh

# set -o xtrace       ## To debug scripts
# set -o errexit      ## To exit on error
# set -o errunset     ## To exit if a variable is referenced but not set


function main() {
    SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
    cd "${SCRIPTPATH}"
    echo "Working Dir: " $(pwd)

    ID=$(podman ps --filter "ancestor=localhost/${CONTAINER}:latest" --format "{{.ID}}")
    if [ "${ID}" == "" ]; then
        echo "Is not up..."
        exit 1
    fi

    podman container stop "${ID}"
}
main $@;
