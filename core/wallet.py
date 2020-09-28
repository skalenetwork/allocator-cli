#   -*- coding: utf-8 -*-
#
#   This file is part of validator-cli
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

import logging

from skale.utils.account_tools import send_ether, send_tokens
from skale.utils.web3_utils import to_checksum_address
from yaspin import yaspin

from core.wallet_tools import save_ledger_wallet_info

from utils.constants import SPIN_COLOR
from utils.web3_utils import init_skale_w_wallet_from_config
from utils.helper import print_err_with_log_path, get_config

logger = logging.getLogger(__name__)


def send_eth(receiver_address, amount, pk_file):
    _send_funds(receiver_address, amount, pk_file, 'eth')


def send_skl(receiver_address, amount, pk_file):
    _send_funds(receiver_address, amount, pk_file, 'skl')


def _send_funds(receiver_address, amount, pk_file, token_type):
    skale = init_skale_w_wallet_from_config(pk_file, manager=True)
    receiver_address = to_checksum_address(receiver_address)
    with yaspin(text='Transferring funds', color=SPIN_COLOR) as sp:
        try:
            if token_type == 'eth':
                send_ether(skale.web3, skale.wallet, receiver_address, amount)
            elif token_type == 'skl':
                send_tokens(skale, skale.wallet, receiver_address, amount)
            msg = '✔ Funds were successfully transferred'
            logger.info(msg)
            sp.write(msg)
        except Exception as err:
            logger.error('Funds were not sent due to error', exc_info=err)
            sp.write('❌ Funds sending failed')
            print_err_with_log_path()


def setup_ledger(address_index, keys_type):
    config = get_config()
    if not config:
        print('You should run < init > first')
        return
    if config['wallet'] != 'ledger':
        print('This command is only available for the Ledger wallet')
        return
    save_ledger_wallet_info(address_index, keys_type)
    print('✔ Ledger wallet setup completed')
