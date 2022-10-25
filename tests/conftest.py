""" SKALE config test """

import os
import subprocess

import pytest
from click.testing import CliRunner

from utils.helper import get_config
from utils.web3_utils import init_skale_w_wallet_from_config

from tests.constants import TEST_PK_FILE, SECOND_TEST_PK_FILE
from tests.helper import get_executable_path
from tests.prepare_data import init_test_skale_manager


@pytest.fixture
def beneficiary_escrow_address(skale_allocator_beneficiary):
    return skale_allocator_beneficiary.allocator.get_escrow_address(
        beneficiary_address=skale_allocator_beneficiary.wallet.address
    )


@pytest.fixture
def skale_manager():
    '''Returns SKALE Manager with provider from config'''
    config = get_config()
    return init_test_skale_manager(endpoint=config['endpoint'], pk_file=TEST_PK_FILE)


@pytest.fixture
def skale_allocator_vm():
    '''Returns SKALE Allocator with vesting manager key'''
    return init_skale_w_wallet_from_config(pk_file=TEST_PK_FILE)


@pytest.fixture
def skale_allocator_beneficiary():
    '''Returns SKALE Allocator with provider from config'''
    return init_skale_w_wallet_from_config(pk_file=SECOND_TEST_PK_FILE)


@pytest.fixture
def runner():
    return CliRunner()


def str_contains(string, values):
    return all(x in string for x in values)


@pytest.fixture(scope='session')
def executable():
    cmd = ['scripts/build.sh', '0.0.0', 'test-branch']
    result = subprocess.run(
        cmd,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ}
    )
    assert result.returncode == 0
    executable_path = get_executable_path()
    try:
        yield executable_path
    finally:
        os.remove(executable_path)
