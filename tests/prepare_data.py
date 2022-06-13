""" Preparation scripts for tests """

from skale.utils.contracts_provision import D_PLAN_ID, MONTH_IN_SECONDS
from skale.utils.contracts_provision.main import (
    add_all_permissions,
    setup_validator,
    set_test_msr,
    set_test_mda,
    _skip_evm_time
)
from skale.utils.contracts_provision.allocator import (
    add_test_plan,
    connect_test_beneficiary,
    send_tokens,
    TEST_SKALE_AMOUNT,
    transfer_tokens_to_allocator
)

from skale.wallets.web3_wallet import generate_wallet
from skale.utils.helper import init_default_logger
from skale.utils.account_tools import send_eth

from utils.web3_utils import init_skale_w_wallet_from_config

from tests.constants import (
    TEST_PK_FILE,
    TEST_ETH_TRANSFER_AMOUNT,
    SECOND_TEST_PK_FILE
)
from tests.helper import init_test_skale_manager


def prepare_beneficiary_wallet(skale_manager):
    wallet = generate_wallet(skale_manager.web3)
    send_eth(
        skale_manager.web3,
        skale_manager.wallet,
        wallet.address,
        TEST_ETH_TRANSFER_AMOUNT
    )
    with open(SECOND_TEST_PK_FILE, "w") as text_file:
        print(wallet._private_key, file=text_file)
    return wallet


def provision_allocator(skale_manager, skale_allocator):
    beneficiary_wallet = prepare_beneficiary_wallet(skale_manager)

    launch_ts = skale_manager.constants_holder.get_launch_timestamp()
    if launch_ts != 0:
        skale_manager.constants_holder.set_launch_timestamp(0)

    vesting_manager_role = skale_allocator.allocator.vesting_manager_role()
    skale_allocator.allocator.grant_role(vesting_manager_role, skale_allocator.wallet.address)

    transfer_tokens_to_allocator(skale_manager, skale_allocator)
    add_test_plan(skale_allocator)

    connect_test_beneficiary(skale_allocator, D_PLAN_ID, beneficiary_wallet)
    send_tokens(
        skale_manager,
        skale_allocator.allocator.get_escrow_address(
            beneficiary_address=beneficiary_wallet.address
        ),
        TEST_SKALE_AMOUNT * 1000
    )
    skale_allocator.allocator.start_vesting(beneficiary_wallet.address)


def main():
    init_default_logger()
    skale_allocator = init_skale_w_wallet_from_config(pk_file=TEST_PK_FILE)
    skale_manager = init_test_skale_manager(skale_allocator._endpoint, TEST_PK_FILE)

    add_all_permissions(skale_manager, skale_manager.wallet.address)

    setup_validator(skale_manager)

    set_test_mda(skale_manager)
    set_test_msr(skale_manager)

    provision_allocator(skale_manager, skale_allocator)
    _skip_evm_time(skale_allocator.web3, MONTH_IN_SECONDS * 12)


if __name__ == '__main__':
    main()
