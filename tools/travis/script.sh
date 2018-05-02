#!/usr/bin/env bash

set -e

export MN_SOURCE=$PWD
export MN_INSTALL=`pip show multinet | grep Location | awk '{print $2"/multinet"}'`

if [[ "${REPORT_COVERAGE}" == 1 ]]; then
    pytest --cov
else
    cd $MN_INSTALL
    printenv PWD
    pytest
    cd $MN_SOURCE
fi

set +e
