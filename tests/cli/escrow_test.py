""" Tests for cli/escrow.py module """

from skale.utils.contracts_provision.main import _skip_evm_time
from skale.utils.contracts_provision import MONTH_IN_SECONDS

from cli.escrow import (
    _delegate
)
from utils.helper import to_wei
# from tests.conftest import str_contains
from tests.constants import (SECOND_TEST_PK_FILE, D_VALIDATOR_ID,
                             D_DELEGATION_PERIOD, D_DELEGATION_INFO, DELEGATION_AMOUNT_SKL)


def _get_number_of_delegations(skale):
    return skale.delegation_controller._get_delegation_ids_len_by_validator(D_VALIDATOR_ID)


def test_delegate(runner, skale_manager, skale_allocator_beneficiary, beneficiary_escrow_address):
    _skip_evm_time(skale_manager.web3, MONTH_IN_SECONDS * (D_DELEGATION_PERIOD + 1))
    num_of_delegations_before = _get_number_of_delegations(skale_manager)

    delegated_amount_before = skale_manager.delegation_controller.get_delegated_amount(
        beneficiary_escrow_address
    )
    result = runner.invoke(
        _delegate,
        [
            '--validator-id', D_VALIDATOR_ID,
            '--amount', DELEGATION_AMOUNT_SKL,
            '--info', D_DELEGATION_INFO,
            '--pk-file', SECOND_TEST_PK_FILE,
            '--yes'
        ]
    )

    delegations = skale_manager.delegation_controller.get_all_delegations_by_validator(
        validator_id=D_VALIDATOR_ID
    )
    delegation_id = delegations[-1]['id']
    skale_manager.delegation_controller.accept_pending_delegation(
        delegation_id,
        wait_for=True
    )
    _skip_evm_time(skale_manager.web3, MONTH_IN_SECONDS * (D_DELEGATION_PERIOD + 1))

    delegated_amount_after = skale_manager.delegation_controller.get_delegated_amount(
        beneficiary_escrow_address
    )
    assert delegated_amount_after == delegated_amount_before + to_wei(DELEGATION_AMOUNT_SKL)

    num_of_delegations_after = _get_number_of_delegations(skale_manager)
    assert num_of_delegations_after == num_of_delegations_before + 1
    assert result.exit_code == 0
