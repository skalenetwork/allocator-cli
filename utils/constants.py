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

import os
import sys
from pathlib import Path


def _get_env():
    try:
        sys._MEIPASS
    except AttributeError:
        return 'dev'
    return 'prod'


ENV = _get_env()
CURRENT_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))

if ENV == 'dev':
    ROOT_DIR = os.path.join(CURRENT_FILE_LOCATION, os.pardir)
else:
    ROOT_DIR = os.path.join(sys._MEIPASS, 'data')

TEXT_FILE = os.path.join(ROOT_DIR, 'text.yml')

LONG_LINE = '-' * 50
SPIN_COLOR = 'yellow'
DISABLE_SPIN = os.getenv('DISABLE_SPIN')

HOME_DIR = str(Path.home())
SKALE_ALLOCATOR_CONFIG_FOLDER = os.path.join(HOME_DIR, '.skale-allocator-cli')
SKALE_ALLOCATOR_CONFIG_FILE = os.path.join(SKALE_ALLOCATOR_CONFIG_FOLDER, 'config.json')
SKALE_ALLOCATOR_LEDGER_INFO_FILE = os.path.join(SKALE_ALLOCATOR_CONFIG_FOLDER, 'ledger_info.json')
SKALE_ALLOCATOR_ABI_FILE = os.path.join(SKALE_ALLOCATOR_CONFIG_FOLDER, 'abi.json')
SGX_DATA_DIR = os.getenv('SGX_DATA_DIR') or os.path.join(SKALE_ALLOCATOR_CONFIG_FOLDER, 'sgx')
SGX_INFO_PATH = os.path.join(SGX_DATA_DIR, 'info.json')
SGX_SSL_CERTS_PATH = os.path.join(SGX_DATA_DIR, 'ssl')

WALLET_TYPES = ['software', 'ledger', 'sgx']
LEDGER_KEYS_TYPES = ['legacy', 'live']
# DELEGATION_PERIOD_OPTIONS = ['3', '6', '9', '12']  # strings because of click.Choice design
DELEGATION_PERIOD_OPTIONS = ['2']  # strings because of click.Choice design

PERMILLE_MULTIPLIER = 10


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOG_FILE_SIZE_MB = 50
LOG_FILE_SIZE_BYTES = LOG_FILE_SIZE_MB * 1000000

LOG_BACKUP_COUNT = 2
LOG_DATA_PATH = os.path.join(SKALE_ALLOCATOR_CONFIG_FOLDER, 'log')
LOG_FILEPATH = os.path.join(LOG_DATA_PATH, 'sk-allocator.log')
DEBUG_LOG_FILEPATH = os.path.join(LOG_DATA_PATH, 'debug-sk-allocator.log')

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
