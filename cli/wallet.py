import logging
import click

from core.wallet import (
    transfer_eth,
    transfer_skl,
    setup_ledger,
    wallet_info
)
from utils.helper import abort_if_false, transaction_cmd
from utils.texts import Texts
from utils.constants import LEDGER_KEYS_TYPES

G_TEXTS = Texts()
TEXTS = G_TEXTS['wallet']

logger = logging.getLogger(__name__)


@click.group()
def wallet_cli():
    pass


@wallet_cli.group('wallet', help=TEXTS['help'])
def wallet():
    pass


@wallet.command('send-eth', help=TEXTS['send_eth']['help'])
@transaction_cmd
@click.argument('receiver_address')
@click.argument('amount')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False, prompt=TEXTS['send_eth']['confirm'])
def _send_eth(receiver_address, amount, pk_file, fee):
    transfer_eth(receiver_address, amount, pk_file, fee=fee)


@wallet.command('send-skl', help=TEXTS['send_skl']['help'])
@click.argument('receiver_address')
@click.argument('amount')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False, prompt=TEXTS['send_skl']['confirm'])
def _send_skl(receiver_address, amount, pk_file, fee):
    transfer_skl(receiver_address, amount, pk_file, fee=fee)


@wallet.command('info', help=TEXTS['info']['help'])
@click.option(
    '--pk-file',
    help=G_TEXTS['pk_file']['help']
)
def info(pk_file):
    wallet_info(pk_file)


@wallet.command('setup-ledger', help=TEXTS['setup_ledger']['help'])
@click.option(
    '--address-index',
    type=int,
    help=G_TEXTS['address_index']['help'],
    prompt=G_TEXTS['address_index']['prompt']
)
@click.option(
    '--keys-type',
    type=click.Choice(LEDGER_KEYS_TYPES),
    help=TEXTS['setup_ledger']['keys_type']['help'],
    prompt=TEXTS['setup_ledger']['keys_type']['prompt']
)
def _setup_ledger(address_index, keys_type):
    setup_ledger(address_index, keys_type)
