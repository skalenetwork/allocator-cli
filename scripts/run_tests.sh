#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR=$(dirname $DIR)

export DISABLE_SPIN=True
export SGX_SERVER_URL='https://127.0.0.1:1026'

export SGX_DATA_DIR='tests/tmp-test-sgx'
export ALLOWED_TS_DIFF=-1000000000000000

python $PROJECT_DIR/tests/prepare_data.py
py.test --cov=$PROJECT_DIR/ $PROJECT_DIR/tests/cli/escrow_test.py $@
