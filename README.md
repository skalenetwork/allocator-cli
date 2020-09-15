# SKALE Allocator CLI

![Build and publish](https://github.com/skalenetwork/allocator-cli/workflows/Build%20and%20publish/badge.svg)
![Test](https://github.com/skalenetwork/allocator-cli/workflows/Test/badge.svg)
[![Discord](https://img.shields.io/discord/534485763354787851.svg)](https://discord.gg/vvUtWJB)

## Table of Contents

1.  [Installation](#installation)
2.  [CLI usage](#cli-usage)  
    2.1 [Init](#init)  
    2.2 [Escrow](#escrow)  
    2.3 [SGX](#sgx)  
3.  [Development](#development)  

## Installation

### Requirements

-   Linux or macOS machine
-   Download executable

```bash
VERSION_NUM={put the version number here} && sudo -E bash -c "curl -L https://github.com/skalenetwork/allocator-cli/releases/download/$VERSION_NUM/sk-alloc-$VERSION_NUM-`uname -s`-`uname -m` >  /usr/local/bin/sk-alloc"
```

-  Apply executable permissions to the binary:

```bash
sudo chmod +x /usr/local/bin/sk-alloc
```

### Where to find out the latest version

All allocator-cli version numbers are available here: https://github.com/skalenetwork/allocator-cli/releases

## CLI Usage

### Init

Download SKALE Allocator contracts info and set the endpoint.

```bash
sk-alloc init
```

Required arguments:

-   `--endpoint/-e` - RPC endpoint of the node in the network where SKALE Allocator is deployed (`ws` or `wss`)
-   `--contracts-url/-c` - - URL to SKALE Allocator contracts ABI and addresses
-   `-w/--wallet` - Type of the wallet that will be used for signing transactions (software, sgx or hardware)

If you want to use sgx wallet you need to initialize it first (see **SGX commands**)

Usage example:

```bash
sk-alloc init -e ws://geth.test.com:8546 -c https://test.com/allocator.json --wallet software
```

### Escrow commands

#### Delegate

Delegate tokens to validator

```bash
sk-alloc escrow delegate
```

Required arguments:

-   `--validator-id` - ID of the validator to delegate
-   `--amount` - Amount of SKALE tokens to delegate
-   `--delegation-period` - Delegation period (in months - only `2` avaliable now)
-   `--info` - Delegation request info

Optional arguments:

-   `--pk-file` - Path to file with private key (only for `software` wallet type)

#### Request undelegation

Request undelegation in the end of delegation period

```bash
sk-alloc escrow undelegate [DELEGATION_ID]
```

Required params:

1) Delegation ID - ID of the delegation

Optional arguments:

-   `--pk-file` - Path to file with private key (only for `software` wallet type)

#### Retrieve tokens

Allows Beneficiary to retrieve vested tokens from the Escrow contract

```bash
sk-alloc escrow retrieve
```

Optional arguments:

-   `--pk-file` - Path to file with private key (only for `software` wallet type)

#### Withdraw bounty

Withdraw earned bounty. Default recipient is the transaction sender.

```bash
sk-alloc escrow withdraw-bounty [VALIDATOR_ID] --pk-file ./pk.txt
```

Required params:

1) VALIDATOR_ID - ID of the validator

Optional arguments:

-   `--recipient-address` - Address of the recipient. Defaults to the sender.  
-   `--pk-file` - Path to file with private key (only for `software` wallet type)
-   `--yes` - Confirmation flag
- `--beneficiary-address` - Address of the beneficiary with Escrow contract

#### Cancel pending delegation

Cancel pending delegation request

```bash
sk-alloc escrow cancel-delegation [DELEGATION_ID]
```

Required params:

1) Delegation ID - ID of the delegation to cancel

Optional arguments:

- `--pk-file` - Path to file with private key (only for `software` wallet type)

#### Beneficiary info

Info about beneficiary by address

```bash
sk-alloc escrow info [ADDRESS]
```

Required params:

1) Address - address of the beneficiary with Escrow

### SGX commands

> Note: SGX wallet is not ready for production use yet.

#### Init 
 Initialize sgx wallet  
 ```bash
sk-alloc sgx init [SGX_SERVER_URL]
```
Optional arguments:
-   `--force/-f` - Rewrite current sgx wallet data
-  `--ssl-port` - Port that is used by sgx server to establish tls connection

#### Info
Print sgx wallet information
```bash
sk-alloc sgx info 
```
Optional arguments:
-   `--raw` - Print info in plain json

## Development

### Setup repo

#### Install development dependencies

```bash
pip install -e .[dev]
```

##### Add flake8 git hook

In file `.git/hooks/pre-commit` add:

```bash
#!/bin/sh
flake8 .
```

### Debugging

Run commands in dev mode:

```bash
python cli/main.py YOUR_COMMAND
```

### License

![GitHub](https://img.shields.io/github/license/skalenetwork/allocator-cli.svg)

All contributions are made under the [GNU Affero General Public License v3](https://www.gnu.org/licenses/agpl-3.0.en.html). See [LICENSE](LICENSE).
