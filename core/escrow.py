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
from skale.transactions.result import TransactionError

from utils.web3_utils import (init_skale_w_wallet_from_config)
from utils.helper import to_wei
from utils.constants import SPIN_COLOR


D_DELEGATION_PERIOD = 3


def delegate(validator_id, amount, delegation_period, info, pk_file):
    skale = init_skale_w_wallet_from_config(pk_file)
    if not skale:
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


def withdraw_bounty(validator_id, recipient_address, pk_file):
    skale = init_skale_w_wallet_from_config(pk_file)
    if not skale:
        return
    if not recipient_address:
        recipient_address = skale.wallet.address
    with yaspin(text='Withdrawing bounty', color=SPIN_COLOR) as sp:
        tx_res = skale.escrow.withdraw_bounty(
            validator_id=validator_id,
            to=recipient_address,
            beneficiary_address=skale.wallet.address,
            raise_for_status=False,
            wait_for=True
        )
        try:
            tx_res.raise_for_status()
        except TransactionError as err:
            sp.write(str(err))
            return
        sp.write(f'✔ Bounty successfully transferred to {recipient_address}')
