#   -*- coding: utf-8 -*-
#
#   This file is part of allocator-cli
#
#   Copyright (C) 2019 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from yaspin import yaspin
from terminaltables import SingleTable

from web3 import Web3
from skale.transactions.result import TransactionError

from utils.web3_utils import init_skale_w_wallet_from_config, init_skale_from_config
from utils.helper import to_wei, from_wei, escrow_exists, print_no_escrow_msg, convert_timestamp
from utils.constants import SPIN_COLOR
from utils.texts import Texts


G_TEXTS = Texts()
D_DELEGATION_PERIOD = 3


def delegate(validator_id, amount, delegation_period, info, pk_file):
    skale = init_skale_w_wallet_from_config(pk_file)

    if not skale:
        return
    if not escrow_exists(skale, skale.wallet.address):
        print_no_escrow_msg(skale.wallet.address)
        return

    with yaspin(text='Sending delegation request', color=SPIN_COLOR) as sp:
        amount_wei = to_wei(amount)
        tx_res = skale.escrow.delegate(
            validator_id=validator_id,
            amount=amount_wei,
            delegation_period=delegation_period,
            info=info,
            beneficiary_address=skale.wallet.address,
            wait_for=True,
            raise_for_status=False
        )
        try:
            tx_res.raise_for_status()
        except TransactionError as err:
            sp.write(str(err))
            return
        sp.write("✔ Delegation request sent")


def undelegate(delegation_id: int, pk_file: str) -> None:
    skale = init_skale_w_wallet_from_config(pk_file)

    if not skale:
        return
    if not escrow_exists(skale, skale.wallet.address):
        print_no_escrow_msg(skale.wallet.address)
        return

    with yaspin(text='Requesting undelegation', color=SPIN_COLOR) as sp:
        tx_res = skale.escrow.request_undelegation(
            delegation_id=delegation_id,
            beneficiary_address=skale.wallet.address,
            wait_for=True,
            raise_for_status=False,
        )
        try:
            tx_res.raise_for_status()
        except TransactionError as err:
            sp.write(str(err))
            return
        sp.write("✔ Successfully undelegated")


def retrieve(pk_file: str) -> None:
    skale = init_skale_w_wallet_from_config(pk_file)

    if not skale:
        return
    if not escrow_exists(skale, skale.wallet.address):
        print_no_escrow_msg(skale.wallet.address)
        return

    with yaspin(text='Retrieving tokens', color=SPIN_COLOR) as sp:
        tx_res = skale.escrow.retrieve(
            beneficiary_address=skale.wallet.address,
            wait_for=True,
            raise_for_status=False,
        )
        try:
            tx_res.raise_for_status()
        except TransactionError as err:
            sp.write(str(err))
            return
        sp.write("✔ Successfully retrieved tokens")


def retrieve_after_termination(address: str, beneficiary_address: str, pk_file: str) -> None:
    skale = init_skale_w_wallet_from_config(pk_file)
    if not skale:
        return
    with yaspin(text='Retrieving tokens after termination', color=SPIN_COLOR) as sp:
        if not beneficiary_address:
            beneficiary_address = skale.wallet.address
        if not escrow_exists(skale, beneficiary_address):
            print_no_escrow_msg(beneficiary_address)
            return
        tx_res = skale.escrow.retrieve_after_termination(
            address=address,
            beneficiary_address=beneficiary_address,
            wait_for=True,
            raise_for_status=False,
        )
        try:
            tx_res.raise_for_status()
        except TransactionError as err:
            sp.write(str(err))
            return
        sp.write("✔ Successfully retrieved tokens")


def withdraw_bounty(validator_id, recipient_address, beneficiary_address, pk_file):
    skale = init_skale_w_wallet_from_config(pk_file)

    if not skale:
        return
    if not recipient_address:
        recipient_address = skale.wallet.address
    if not beneficiary_address:
        beneficiary_address = skale.wallet.address
    if not escrow_exists(skale, beneficiary_address):
        print_no_escrow_msg(beneficiary_address)
        return

    with yaspin(text='Withdrawing bounty', color=SPIN_COLOR) as sp:
        tx_res = skale.escrow.withdraw_bounty(
            validator_id=validator_id,
            to=recipient_address,
            beneficiary_address=beneficiary_address,
            raise_for_status=False,
            wait_for=True
        )
        try:
            tx_res.raise_for_status()
        except TransactionError as err:
            sp.write(str(err))
            return
        sp.write(f'✔ Bounty successfully transferred to {recipient_address}')


def cancel_pending_delegation(delegation_id: int, pk_file: str) -> None:
    skale = init_skale_w_wallet_from_config(pk_file)

    if not skale:
        return
    if not escrow_exists(skale, skale.wallet.address):
        print_no_escrow_msg(skale.wallet.address)
        return

    with yaspin(text='Canceling delegation request', color=SPIN_COLOR) as sp:
        tx_res = skale.escrow.cancel_pending_delegation(
            delegation_id=delegation_id,
            beneficiary_address=skale.wallet.address,
            raise_for_status=False
        )
        try:
            tx_res.raise_for_status()
        except TransactionError as err:
            sp.write(str(err))
            return
        sp.write("✔ Delegation request canceled")


def info(beneficiary_address: str, wei: bool) -> None:
    skale = init_skale_from_config()
    address_fx = Web3.toChecksumAddress(beneficiary_address)

    if not skale:
        return
    if not escrow_exists(skale, address_fx):
        print_no_escrow_msg(address_fx)
        return

    plan_params = skale.allocator.get_beneficiary_plan_params(address_fx)
    escrow_address = skale.allocator.get_escrow_address(address_fx)

    vested_amount = skale.allocator.calculate_vested_amount(address_fx)
    finish_vesting_time = skale.allocator.get_finish_vesting_time(address_fx)
    lockup_period_end_timestamp = skale.allocator.get_lockup_period_end_timestamp(address_fx)
    time_of_next_vest = skale.allocator.get_time_of_next_vest(address_fx)
    is_vesting_active = skale.allocator.is_vesting_active(address_fx)

    # m_type = 'SKL - wei' if wei else 'SKL'
    if wei:
        full_amount = plan_params['fullAmount']
        amount_after_lockup = plan_params['amountAfterLockup']
    else:
        full_amount = from_wei(plan_params['fullAmount'])
        amount_after_lockup = from_wei(plan_params['amountAfterLockup'])
        vested_amount = from_wei(vested_amount)

    table = SingleTable([
        ['Beneficiary address', beneficiary_address],
        ['Escrow address', escrow_address],
        ['Status', plan_params['statusName']],
        ['Plan ID', plan_params['planId']],
        ['Start month', plan_params['startMonth']],
        ['Full amount', full_amount],
        ['Amount after lockup', amount_after_lockup],
        ['Vested amount', vested_amount],
        ['Finish vesting time', convert_timestamp(finish_vesting_time)],
        ['Lockup period end', convert_timestamp(lockup_period_end_timestamp)],
        ['Time of next vest', convert_timestamp(time_of_next_vest)],
        ['Vesting active', is_vesting_active]
    ])
    print(table.table)
