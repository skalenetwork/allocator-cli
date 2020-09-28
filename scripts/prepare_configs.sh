#!/usr/bin/env bash

set -e

: "${ETH_PRIVATE_KEY?Need to set ETH_PRIVATE_KEY}"
: "${ENDPOINT?Need to set ENDPOINT}"

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

CLI_CONFIG_FOLDER=$HOME/.skale-allocator-cli
CLI_ABI_FILE=$CLI_CONFIG_FOLDER/abi.json
CLI_ABI_CONFIG=$CLI_CONFIG_FOLDER/config.json
TEST_PK_FILE=$DIR/../tests/test-pk.txt

mkdir -p $CLI_CONFIG_FOLDER
cp $DIR/../helper-scripts/contracts_data/universal.json $CLI_ABI_FILE

ENDPOINT='http://localhost:8545'
echo {\"endpoint\": \"${ENDPOINT}\",\"wallet\": \"software\"} > $CLI_ABI_CONFIG
echo $ETH_PRIVATE_KEY > $TEST_PK_FILE
