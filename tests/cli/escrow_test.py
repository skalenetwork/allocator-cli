""" Tests for cli/escrow.py module """

from skale.utils.contracts_provision import MONTH_IN_SECONDS, D_PLAN_ID
from skale.utils.contracts_provision.allocator import connect_test_beneficiary
from skale.utils.contracts_provision.main import _skip_evm_time
from skale.wallets.web3_wallet import generate_wallet

from cli.escrow import (
    _delegate,
    _undelegate,
    _retrieve,
    _withdraw_bounty,
    _cancel_delegation,
    _retrieve_after_termination,
    _info,
    _plan_info,
    _delegations,
    _validators
)
from utils.helper import to_wei
from tests.helper import check_validator_fields, convert_validators_info, str_contains
from tests.constants import (
    DELEGATION_AMOUNT_SKL,
    D_VALIDATOR_ID,
    D_DELEGATION_AMOUNT,
    D_DELEGATION_INFO,
    D_DELEGATION_PERIOD,
    SECOND_TEST_PK_FILE,
    TEST_PK_FILE
)


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


def test_info(runner, skale_allocator_beneficiary):
    from core.escrow import info as core_info
    out = core_info(skale_allocator_beneficiary.wallet.address)
    print(out)
    result = runner.invoke(
        _info,
        [
            skale_allocator_beneficiary.wallet.address
        ]
    )
    output_list = result.output.splitlines()
    assert result.exit_code == 0
    escrow_address = skale_allocator_beneficiary.allocator.get_escrow_address(
        skale_allocator_beneficiary.wallet.address
    )

    assert f'\x1b(0x\x1b(B Beneficiary address \x1b(0x\x1b(B {skale_allocator_beneficiary.wallet.address} \x1b(0x\x1b(B' in output_list # noqa
    assert f'\x1b(0x\x1b(B Escrow address      \x1b(0x\x1b(B {escrow_address} \x1b(0x\x1b(B' in output_list  # noqa
    assert '\x1b(0x\x1b(B Status              \x1b(0x\x1b(B ACTIVE                                     \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Plan ID             \x1b(0x\x1b(B 1                                          \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Start month         \x1b(0x\x1b(B 8                                          \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Full amount         \x1b(0x\x1b(B 5000                                       \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Amount after lockup \x1b(0x\x1b(B 1000                                       \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Finish vesting time \x1b(0x\x1b(B 01.09.2023                                 \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Lockup period end   \x1b(0x\x1b(B 01.03.2021                                 \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Vesting active      \x1b(0x\x1b(B True                                       \x1b(0x\x1b(B' in output_list # noqa


def test_delegate(runner, skale_manager, beneficiary_escrow_address, skale_allocator_beneficiary):
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
    skale_manager.delegation_controller.accept_pending_delegation(delegation_id)
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


def test_cancel_delegation(
    runner,
    skale_manager,
    beneficiary_escrow_address,
    skale_allocator_beneficiary
):
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
    assert result.exit_code == 0

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


def test_plan_info(runner, skale_allocator_beneficiary):
    result = runner.invoke(
        _plan_info,
        [
            '1'
        ]
    )
    output_list = result.output.splitlines()

    assert '\x1b(0x\x1b(B Plan ID                    \x1b(0x\x1b(B 1    \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Total vesting duration     \x1b(0x\x1b(B 36   \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Vesting cliff              \x1b(0x\x1b(B 6    \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Vesting interval time unit \x1b(0x\x1b(B 1    \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Vesting interval           \x1b(0x\x1b(B 6    \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Is delegation allowed      \x1b(0x\x1b(B True \x1b(0x\x1b(B' in output_list # noqa
    assert '\x1b(0x\x1b(B Is terminatable            \x1b(0x\x1b(B True \x1b(0x\x1b(B' in output_list # noqa


def test_ls(runner, skale_manager):
    result = runner.invoke(_validators)
    output_list = result.output.splitlines()

    validators_info = skale_manager.validator_service.ls()
    converted_info = convert_validators_info(validators_info)
    expected_info = list(filter(lambda v: v['status'] == 'Trusted',
                                converted_info))

    header = list(filter(lambda s: s.strip().startswith('Name'), output_list))
    assert len(header) == 1
    pos = output_list.index(header[0])
    actual_info = output_list[pos + 2:]

    fields = ['name', 'id', 'validator_address', 'description', 'fee_rate',
              'registration_time', 'minimum_delegation_amount',
              'status']
    assert len(actual_info) == len(expected_info)
    for plain_actual, expected in zip(actual_info, expected_info):
        actual = plain_actual.split()
        check_validator_fields(expected, actual, fields)

    assert result.exit_code == 0


def test_delegations_skl(runner, skale_manager, skale_allocator_beneficiary):
    result = runner.invoke(
        _delegations,
        [skale_allocator_beneficiary.wallet.address]
    )
    output_list = result.output.splitlines()
    delegation = skale_manager.delegation_controller.get_delegation(0)

    escrow_address = skale_allocator_beneficiary.allocator.get_escrow_address(
        skale_allocator_beneficiary.wallet.address
    )

    assert output_list[0] == f'Delegations for address {skale_allocator_beneficiary.wallet.address} (Escrow: {escrow_address}):' # noqa
    assert str_contains(output_list[2], [
        'Id', 'Delegator Address', 'Status', 'Validator Id', 'Amount (SKL)',
        'Delegation period (months)', 'Created At', 'Info'
    ])
    assert str_contains(output_list[4], [
        escrow_address, delegation['info']
    ])
    assert result.exit_code == 0
