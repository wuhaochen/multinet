#!/usr/bin/env bash

set -e

pip install --upgrade pytest pytest-cov codecov

if [[ "${REPORT_COVERAGE}" == 1 ]]; then
    pip install -e .;
else
    pip install .;
fi

set +e
