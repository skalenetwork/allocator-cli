# SKALE Allocator CLI

![Build and publish](https://github.com/skalenetwork/allocator-cli/workflows/Build%20and%20publish/badge.svg)
![Test](https://github.com/skalenetwork/allocator-cli/workflows/Test/badge.svg)
[![Discord](https://img.shields.io/discord/534485763354787851.svg)](https://discord.gg/vvUtWJB)

## Table of Contents

1.  [Installation](#installation)
2.  [CLI usage](#cli-usage)  
    2.1 [Init](#init)
3.  [Development](#development)  

## Installation

### Requirements

-   Linux or macOS machine
-   Download executable

```bash
VERSION_NUM={put the version number here} && sudo -E bash -c "curl -L https://allocator-cli.sfo2.digitaloceanspaces.com/develop/sk-alloc-$VERSION_NUM-`uname -s`-`uname -m` >  /usr/local/bin/sk-alloc"
```

-   Apply executable permissions to the binary:

```bash
chmod +x /usr/local/bin/sk-alloc
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

### SGX commands

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
