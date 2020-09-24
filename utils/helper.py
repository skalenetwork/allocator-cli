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
import json
import urllib
import datetime
import logging

from web3 import Web3

from utils.texts import Texts
from utils.constants import (SKALE_ALLOCATOR_CONFIG_FILE, SKALE_ALLOCATOR_ABI_FILE,
                             PERMILLE_MULTIPLIER, ZERO_ADDRESS, DEBUG_LOG_FILEPATH)


G_TEXTS = Texts()
logger = logging.getLogger(__name__)


def safe_mk_dirs(path):
    if os.path.exists(path):
        return
    logger.info(f'Creating {path} directory')
    os.makedirs(path, exist_ok=True)


def read_json(path):
    with open(path, encoding='utf-8') as data_file:
        return json.loads(data_file.read())


def write_json(path, content):
    with open(path, 'w') as outfile:
        json.dump(content, outfile, indent=4)


def download_file(url, filepath):
    try:
        return urllib.request.urlretrieve(url, filepath)
    except urllib.error.HTTPError:
        print(f'Couldn\'t donwload file: {url}')


def config_exists():
    return os.path.exists(SKALE_ALLOCATOR_CONFIG_FILE)


def read_config():
    config = read_json(SKALE_ALLOCATOR_CONFIG_FILE)
    config['abi'] = read_json(SKALE_ALLOCATOR_ABI_FILE)
    return config


def get_config():
    if config_exists():
        return read_config()


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


def to_skl(wei):  # todo: replace with from_wei()
    return Web3.fromWei(wei, 'ether')


def from_wei(val):
    return Web3.fromWei(val, 'ether')


def to_wei(val):
    return Web3.toWei(val, 'ether')


def permille_to_percent(val):
    return int(val) / PERMILLE_MULTIPLIER


def percent_to_permille(val):
    return int(val * PERMILLE_MULTIPLIER)


def escrow_exists(skale, address):
    return skale.allocator.get_escrow_address(address) != ZERO_ADDRESS


def print_no_escrow_msg(address):
    print(f'\n{G_TEXTS["no_escrow"]}: {address}')


def convert_timestamp(timestamp):
    dt = datetime.datetime.utcfromtimestamp(int(timestamp))
    return dt.strftime('%d.%m.%Y')


def print_err_with_log_path(e=''):
    print(e, f'\nPlease check logs: {DEBUG_LOG_FILEPATH}')
