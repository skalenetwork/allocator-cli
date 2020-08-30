""" SKALE config test """

import pytest
from click.testing import CliRunner

from utils.helper import get_config
from utils.web3_utils import init_skale_w_wallet_from_config

from tests.constants import TEST_PK_FILE, SECOND_TEST_PK_FILE
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
def skale_allocator_beneficiary():
    '''Returns SKALE Allocator with provider from config'''
    return init_skale_w_wallet_from_config(pk_file=SECOND_TEST_PK_FILE)


@pytest.fixture
def runner():
    return CliRunner()


def str_contains(string, values):
    return all(x in string for x in values)
