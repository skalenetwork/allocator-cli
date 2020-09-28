from skale.utils.web3_utils import to_checksum_address

from cli.wallet import _send_eth, _send_skl
from tests.constants import TEST_PK_FILE


def test_send_eth(runner, skale_manager):
    address = skale_manager.wallet.address
    amount = '0.01'
    amount_wei = skale_manager.web3.toWei(amount, 'ether')

    receiver_0 = '0xf38b5dddd74b8901c9b5fb3ebd60bf5e7c1e9763'
    checksum_receiver_0 = to_checksum_address(receiver_0)
    receiver_balance_0 = skale_manager.web3.eth.getBalance(checksum_receiver_0)
    balance_0 = skale_manager.web3.eth.getBalance(address)
    result = runner.invoke(
        _send_eth,
        [
            receiver_0,
            amount,
            '--pk-file', TEST_PK_FILE,
            '--yes'
        ]
    )

    output_list = result.output.splitlines()
    assert result.exit_code == 0
    assert '✔ Funds were successfully transferred' in str(output_list)

    balance_1 = skale_manager.web3.eth.getBalance(address)
    assert balance_1 < balance_0
    assert skale_manager.web3.eth.getBalance(checksum_receiver_0) - receiver_balance_0 == amount_wei

    receiver_1 = '0x01C19c5d3Ad1C3014145fC82263Fbae09e23924A'
    receiver_balance_1 = skale_manager.web3.eth.getBalance(receiver_1)
    result = runner.invoke(
        _send_eth,
        [
            receiver_1,
            amount,
            '--pk-file', TEST_PK_FILE,
            '--yes'
        ]
    )

    output_list = result.output.splitlines()
    print(output_list)
    assert result.exit_code == 0
    assert '✔ Funds were successfully transferred' in str(output_list)
    assert skale_manager.web3.eth.getBalance(address) < balance_1
    assert skale_manager.web3.eth.getBalance(receiver_1) - receiver_balance_1 == amount_wei


def test_send_skl(runner):
    result = runner.invoke(
        _send_skl,
        [
            '0x01C19c5d3Ad1C3014145fC82263Fbae09e23924A',
            '0.01',
            '--pk-file', TEST_PK_FILE,
            '--yes'
        ]
    )
    output_list = result.output.splitlines()
    assert result.exit_code == 0
    assert '✔ Funds were successfully transferred' in str(output_list)
