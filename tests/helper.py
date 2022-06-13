import copy
import os
from datetime import datetime

from skale import SkaleManager
from skale.utils.web3_utils import init_web3
from skale.wallets import Web3Wallet

from utils.helper import from_wei, permille_to_percent

from tests.constants import DIST_DIR, TEST_SKALE_MANAGER_ABI_PATH


def check_validator_fields(expected, actual, fields):
    for i, field in enumerate(fields):
        assert str(actual[i]) == str(expected[field])


def convert_validators_info(validator_info):
    result = []
    for data in validator_info:
        info = copy.deepcopy(data)
        info['fee_rate'] = permille_to_percent(info['fee_rate'])
        info['minimum_delegation_amount'] = from_wei(
            info['minimum_delegation_amount']
        )
        info['status'] = 'Trusted' if info['trusted'] else 'Registered'
        info['registration_time'] = datetime.fromtimestamp(
            info['registration_time']
        ).strftime('%d.%m.%Y-%H:%M:%S')
        result.append(info)
    return result


def str_contains(string, values):
    return all(x in string for x in values)


def get_executable_name():
    return os.listdir(DIST_DIR)[0]


def get_executable_path():
    return os.path.join(DIST_DIR, get_executable_name())


def init_test_skale_manager(endpoint, pk_file):
    with open(pk_file, 'r') as f:
        pk = str(f.read()).strip()
    web3 = init_web3(endpoint)
    wallet = Web3Wallet(pk, web3)
    return SkaleManager(endpoint, TEST_SKALE_MANAGER_ABI_PATH, wallet)
