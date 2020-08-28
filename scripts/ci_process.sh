#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR=$(dirname $DIR)

export ENDPOINT=http://localhost:8545

# bash $PROJECT_DIR/helper-scripts/deploy_test_allocator.sh
bash $PROJECT_DIR/scripts/prepare_configs.sh
bash $PROJECT_DIR/scripts/run_tests.sh
