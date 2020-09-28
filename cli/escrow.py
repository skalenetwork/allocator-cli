#   -*- coding: utf-8 -*-
#
#   This file is part of allocator-cli
#
#   Copyright (C) 2020 SKALE Labs
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

import click

from core.escrow import (delegate, undelegate, retrieve, withdraw_bounty, plan_info,
                         cancel_pending_delegation, retrieve_after_termination, info, delegations,
                         validators_list)

from utils.helper import abort_if_false, to_wei
from utils.constants import DELEGATION_PERIOD_OPTIONS
from utils.validations import EthAddressType, UrlType, FloatPercentageType
from utils.texts import Texts


ETH_ADDRESS_TYPE = EthAddressType()
FLOAT_PERCENTAGE_TYPE = FloatPercentageType()
URL_TYPE = UrlType()

G_TEXTS = Texts()
TEXTS = G_TEXTS['escrow']


@click.group()
def escrow_cli():
    pass


@escrow_cli.group('escrow', help="Escrow contract commands")
def escrow():
    pass


@escrow.command('delegate', help=TEXTS['delegate']['help'])
@click.option(
    '--validator-id',
    type=int,
    help=TEXTS['delegate']['validator_id']['help'],
    prompt=TEXTS['delegate']['validator_id']['prompt']
)
@click.option(
    '--amount',
    type=int,
    help=TEXTS['delegate']['amount']['help'],
    prompt=TEXTS['delegate']['amount']['prompt']
)
@click.option(
    '--delegation-period',
    type=click.Choice(DELEGATION_PERIOD_OPTIONS),
    help=TEXTS['delegate']['delegation_period']['help'],
    prompt=TEXTS['delegate']['delegation_period']['prompt']
)
@click.option(
    '--info',
    type=str,
    help=TEXTS['delegate']['info']['help']
    # prompt=TEXTS['delegate']['info']['prompt']
)
@click.option(
    '--pk-file',
    help=G_TEXTS['pk_file']['help']
)
@click.option(
    '--gas-price',
    type=float,
    help=G_TEXTS['gas_price']['help']
)
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt=TEXTS['delegate']['confirm'])
def _delegate(validator_id, amount, delegation_period, info, pk_file,
              gas_price):
    if info is None:
        info = ''
    delegate(
        validator_id=validator_id,
        amount=amount,
        delegation_period=int(delegation_period),
        info=info,
        pk_file=pk_file,
        gas_price=to_wei(gas_price, 'gwei')
    )


@escrow.command('undelegate', help=TEXTS['undelegate']['help'])
@click.argument('delegation_id')
@click.option(
    '--pk-file',
    help=G_TEXTS['pk_file']['help']
)
@click.option(
    '--gas-price',
    type=float,
    help=G_TEXTS['gas_price']['help']
)
def _undelegate(delegation_id, pk_file, gas_price):
    undelegate(
        delegation_id=int(delegation_id),
        pk_file=pk_file,
        gas_price=to_wei(gas_price, 'gwei')
    )


@escrow.command('retrieve', help=TEXTS['retrieve']['help'])
@click.option(
    '--pk-file',
    help=G_TEXTS['pk_file']['help']
)
@click.option(
    '--gas-price',
    type=float,
    help=G_TEXTS['gas_price']['help']
)
def _retrieve(pk_file, gas_price):
    retrieve(
        pk_file=pk_file,
        gas_price=to_wei(gas_price, 'gwei')
    )


@escrow.command('retrieve-after-termination', hidden=True)
@click.option(
    '--address',
    help=TEXTS['retrieve_after_termination']['address']['help'],
    prompt=TEXTS['retrieve_after_termination']['address']['prompt']
)
@click.option(
    '--beneficiary-address',
    help=TEXTS['retrieve_after_termination']['beneficiary_address']['help']
)
@click.option(
    '--pk-file',
    help=G_TEXTS['pk_file']['help']
)
@click.option(
    '--gas-price',
    type=float,
    help=G_TEXTS['gas_price']['help']
)
def _retrieve_after_termination(address, beneficiary_address, pk_file,
                                gas_price):
    retrieve_after_termination(
        address=address,
        beneficiary_address=beneficiary_address,
        pk_file=pk_file,
        gas_price=to_wei(gas_price, 'gwei')
    )


@escrow.command('withdraw-bounty', help=TEXTS['withdraw_bounty']['help'])
@click.argument('validator_id')
@click.option(
    '--recipient-address',
    help=TEXTS['withdraw_bounty']['recipient_address']['help']
)
@click.option(
    '--beneficiary-address',
    help=TEXTS['withdraw_bounty']['beneficiary_address']['help']
)
@click.option(
    '--pk-file',
    help=G_TEXTS['pk_file']['help']
)
@click.option(
    '--gas-price',
    type=float,
    help=G_TEXTS['gas_price']['help']
)
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt=TEXTS['withdraw_bounty']['confirm'])
def _withdraw_bounty(validator_id, recipient_address, beneficiary_address,
                     pk_file, gas_price):
    withdraw_bounty(
        int(validator_id), recipient_address, beneficiary_address,
        pk_file=pk_file,
        gas_price=to_wei(gas_price, 'gwei')
    )


@escrow.command('cancel-delegation', help=TEXTS['cancel_delegation']['help'])
@click.argument('delegation_id')
@click.option(
    '--pk-file',
    help=G_TEXTS['pk_file']['help']
)
@click.option(
    '--gas-price',
    type=float,
    help=G_TEXTS['gas_price']['help']
)
def _cancel_delegation(delegation_id, pk_file, gas_price):
    cancel_pending_delegation(
        delegation_id=int(delegation_id),
        pk_file=pk_file,
        gas_price=to_wei(gas_price, 'gwei')
    )


@escrow.command('info', help=TEXTS['info']['help'])
@click.argument('address')
@click.option('--wei', '-w', is_flag=True, help=G_TEXTS['wei']['help'])
def _info(address, wei):
    info(
        beneficiary_address=address,
        wei=wei
    )


@escrow.command('plan-info', help=TEXTS['plan_info']['help'])
@click.argument('plan_id')
def _plan_info(plan_id):
    plan_info(
        plan_id=int(plan_id)
    )


@escrow.command('delegations', help=TEXTS['delegations']['help'])
@click.argument('address')
@click.option('--wei', '-w', is_flag=True, help=TEXTS['delegations']['wei']['help'])
def _delegations(address, wei):
    delegations(address, wei)


@escrow.command('validators', help=TEXTS['validators']['help'])
@click.option('--wei', '-w', is_flag=True, help=TEXTS['validators']['wei']['help'])
@click.option('--all', is_flag=True)
def _validators(wei, all):
    validators_list(wei, all)
