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
    if [ "${ID}" != "" ]; then
        echo "Is up..."
        exit 1
    fi

    CODE_HOST="${HOME}/Coding"
    CODE_CONTAINER="${HOME}/Coding"
    CONFIG_HOST="${HOME}/.config/lsps"
    CONFIG_CONTAINER="${HOME}/.config/lsps"

    # podman run -d -m 4G \
    podman run -m 4G \
        -p 9999:9999 \
        -e HOME="${HOME}" \
        -e MAVEN_OPTS="-Duser.home=${HOME}" \
        -e JAVA_TOOL_OPTIONS="-Duser.home=${HOME}" \
        -e JDTLS_CONFIG_PATH="${CONFIG_CONTAINER}/jdtls" \
        -e JDTLS_DATA_PATH="${JDTLS_CONFIG_PATH}/data" \
        -v "${CODE_HOST}":"${CODE_CONTAINER}" \
        -v "${CONFIG_HOST}":"${CONFIG_CONTAINER}" \
        "${CONTAINER}:latest"
}
main $@;
