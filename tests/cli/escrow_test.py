""" Tests for cli/escrow.py module """

from skale.wallets.web3_wallet import generate_wallet
from skale.utils.contracts_provision.main import _skip_evm_time
from skale.utils.contracts_provision import MONTH_IN_SECONDS, D_PLAN_ID
from skale.utils.contracts_provision.allocator import connect_test_beneficiary

from cli.escrow import (
    _delegate, _undelegate, _retrieve, _withdraw_bounty, _cancel_delegation,
    _retrieve_after_termination
)
from utils.helper import to_wei
from tests.constants import (TEST_PK_FILE, SECOND_TEST_PK_FILE, D_VALIDATOR_ID, D_DELEGATION_AMOUNT,
                             D_DELEGATION_PERIOD, D_DELEGATION_INFO, DELEGATION_AMOUNT_SKL)


def _get_number_of_delegations(skale):
    return skale.delegation_controller._get_delegation_ids_len_by_validator(D_VALIDATOR_ID)


def _delegate_via_escrow(skale_allocator_beneficiary):
    skale_allocator_beneficiary.escrow.delegate(
        validator_id=D_VALIDATOR_ID,
        amount=D_DELEGATION_AMOUNT,
        delegation_period=D_DELEGATION_PERIOD,
        info=D_DELEGATION_INFO,
        beneficiary_address=skale_allocator_beneficiary.wallet.address,
        wait_for=True
    )


def _generate_and_terminate(skale_allocator_vm):
    wallet = generate_wallet(skale_allocator_vm.web3)
    connect_test_beneficiary(skale_allocator_vm, D_PLAN_ID, wallet)
    skale_allocator_vm.allocator.start_vesting(wallet.address, wait_for=True)
    skale_allocator_vm.allocator.stop_vesting(wallet.address)
    return wallet


def test_delegate(runner, skale_manager, beneficiary_escrow_address):
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
            '--delegation-period', str(D_DELEGATION_PERIOD),
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


def test_undelegate(runner, skale_manager, skale_allocator_beneficiary):
    _delegate_via_escrow(skale_allocator_beneficiary)

    delegations = skale_manager.delegation_controller.get_all_delegations_by_validator(
        validator_id=D_VALIDATOR_ID
    )
    delegation_id = delegations[-1]['id']
    skale_manager.delegation_controller.accept_pending_delegation(
        delegation_id,
        wait_for=True
    )
    _skip_evm_time(skale_manager.web3, MONTH_IN_SECONDS * (D_DELEGATION_PERIOD + 1))

    result = runner.invoke(
        _undelegate,
        [
            str(delegation_id),
            '--pk-file', SECOND_TEST_PK_FILE
        ]
    )

    delegations = skale_manager.delegation_controller.get_all_delegations_by_validator(
        validator_id=D_VALIDATOR_ID
    )
    assert delegations[-1]['id'] == delegation_id
    assert delegations[-1]['status'] == 'UNDELEGATION_REQUESTED'
    assert result.exit_code == 0


def test_retrieve(runner, skale_manager, skale_allocator_beneficiary):
    _delegate_via_escrow(skale_allocator_beneficiary)

    delegations = skale_manager.delegation_controller.get_all_delegations_by_validator(
        validator_id=D_VALIDATOR_ID
    )
    delegation_id = delegations[-1]['id']
    skale_manager.delegation_controller.accept_pending_delegation(
        delegation_id,
        wait_for=True
    )
    _skip_evm_time(skale_manager.web3, MONTH_IN_SECONDS * (D_DELEGATION_PERIOD + 1))

    result = runner.invoke(
        _retrieve,
        [
            '--pk-file', SECOND_TEST_PK_FILE
        ]
    )

    output_list = result.output.splitlines()
    expected_output = '\x1b[K✔ Successfully retrieved tokens'
    assert expected_output in output_list
    assert result.exit_code == 0


def test_retrieve_after_termination(runner, skale_allocator_vm):
    wallet = _generate_and_terminate(skale_allocator_vm)
    result = runner.invoke(
        _retrieve_after_termination,
        [
            '--address', skale_allocator_vm.wallet.address,
            '--beneficiary-address', wallet.address,
            '--pk-file', TEST_PK_FILE
        ]
    )

    output_list = result.output.splitlines()
    expected_output = '\x1b[K✔ Successfully retrieved tokens'
    assert expected_output in output_list
    assert result.exit_code == 0


def test_withdraw_bounty_to_sender(runner, skale_allocator_beneficiary):
    _skip_evm_time(skale_allocator_beneficiary.web3, MONTH_IN_SECONDS * 3)
    result = runner.invoke(
        _withdraw_bounty,
        [
            str(D_VALIDATOR_ID),
            '--pk-file', SECOND_TEST_PK_FILE,
            '--yes'
        ]
    )
    output_list = result.output.splitlines()
    expected_output = f'\x1b[K✔ Bounty successfully transferred to {skale_allocator_beneficiary.wallet.address}' # noqa
    assert expected_output in output_list
    assert result.exit_code == 0


def test_withdraw_bounty_to_custom_address(runner, skale_allocator_beneficiary):
    _skip_evm_time(skale_allocator_beneficiary.web3, MONTH_IN_SECONDS * 3)
    wallet = generate_wallet(skale_allocator_beneficiary.web3)
    recipient_address = wallet.address
    result = runner.invoke(
        _withdraw_bounty,
        [
            str(D_VALIDATOR_ID),
            '--recipient-address', recipient_address,
            '--pk-file', SECOND_TEST_PK_FILE,
            '--yes'
        ]
    )
    output_list = result.output.splitlines()
    expected_output = f'\x1b[K✔ Bounty successfully transferred to {recipient_address}'
    assert expected_output in output_list
    assert result.exit_code == 0


def test_withdraw_bounty_from_vesting_manager(runner, skale_allocator_vm):
    wallet = _generate_and_terminate(skale_allocator_vm)
    result = runner.invoke(
        _withdraw_bounty,
        [
            str(D_VALIDATOR_ID),
            '--beneficiary-address', wallet.address,
            '--pk-file', TEST_PK_FILE,
            '--yes'
        ]
    )
    output_list = result.output.splitlines()
    expected_output = f'\x1b[K✔ Bounty successfully transferred to {skale_allocator_vm.wallet.address}' # noqa
    assert expected_output in output_list
    assert result.exit_code == 0


def test_cancel_delegation(runner, skale_manager):
    result = runner.invoke(
        _delegate,
        [
            '--validator-id', D_VALIDATOR_ID,
            '--amount', DELEGATION_AMOUNT_SKL,
            '--delegation-period', str(D_DELEGATION_PERIOD),
            '--info', D_DELEGATION_INFO,
            '--pk-file', SECOND_TEST_PK_FILE,
            '--yes'
        ]
    )

    delegations = skale_manager.delegation_controller.get_all_delegations_by_validator(
        validator_id=D_VALIDATOR_ID
    )
    delegation_id = delegations[-1]['id']
    assert delegations[-1]['status'] == 'PROPOSED'

    result = runner.invoke(
        _cancel_delegation,
        [
            str(delegation_id),
            '--pk-file', SECOND_TEST_PK_FILE
        ]
    )

    delegations = skale_manager.delegation_controller.get_all_delegations_by_validator(
        validator_id=D_VALIDATOR_ID
    )
    assert delegations[-1]['id'] == delegation_id
    assert delegations[-1]['status'] == 'CANCELED'
    assert result.exit_code == 0
    _skip_evm_time(skale_manager.web3, MONTH_IN_SECONDS)
