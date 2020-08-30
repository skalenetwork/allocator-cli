""" Preparation scripts for tests """

from skale import SkaleManager
from skale.utils.contracts_provision import D_PLAN_ID, MONTH_IN_SECONDS
from skale.utils.contracts_provision.main import (
    setup_validator, set_test_msr, set_test_mda, _skip_evm_time
)
from skale.utils.contracts_provision.allocator import (add_test_plan, transfer_tokens_to_allocator,
                                                       connect_test_beneficiary)

from skale.wallets.web3_wallet import generate_wallet, Web3Wallet
from skale.utils.helper import init_default_logger
from skale.utils.web3_utils import init_web3
from skale.utils.account_tools import send_ether

from tests.constants import (TEST_PK_FILE, TEST_SKALE_MANAGER_ABI_PATH, TEST_ETH_TRANSFER_AMOUNT,
                             SECOND_TEST_PK_FILE)
from utils.web3_utils import init_skale_w_wallet_from_config


def init_test_skale_manager(endpoint, pk_file):
    with open(pk_file, 'r') as f:
        pk = str(f.read()).strip()
    web3 = init_web3(endpoint)
    wallet = Web3Wallet(pk, web3)
    return SkaleManager(endpoint, TEST_SKALE_MANAGER_ABI_PATH, wallet)


def prepare_beneficiary_wallet(skale_manager):
    wallet = generate_wallet(skale_manager.web3)
    send_ether(skale_manager.web3, skale_manager.wallet, wallet.address, TEST_ETH_TRANSFER_AMOUNT)
    with open(SECOND_TEST_PK_FILE, "w") as text_file:
        print(wallet._private_key, file=text_file)
    return wallet


def provision_allocator(skale_manager, skale_allocator):
    beneficiary_wallet = prepare_beneficiary_wallet(skale_manager)

    launch_ts = skale_manager.constants_holder.get_launch_timestamp()
    if launch_ts != 0:
        skale_manager.constants_holder.set_launch_timestamp(0, wait_for=True)

    transfer_tokens_to_allocator(skale_manager, skale_allocator)
    add_test_plan(skale_allocator)

    connect_test_beneficiary(skale_allocator, D_PLAN_ID, beneficiary_wallet)
    skale_allocator.allocator.start_vesting(beneficiary_wallet.address, wait_for=True)


def main():
    init_default_logger()
    skale_allocator = init_skale_w_wallet_from_config(pk_file=TEST_PK_FILE)
    skale_manager = init_test_skale_manager(skale_allocator._endpoint, TEST_PK_FILE)

    setup_validator(skale_manager)

    set_test_mda(skale_manager)
    set_test_msr(skale_manager)

    provision_allocator(skale_manager, skale_allocator)
    _skip_evm_time(skale_allocator.web3, MONTH_IN_SECONDS * 12)


if __name__ == '__main__':
    main()
