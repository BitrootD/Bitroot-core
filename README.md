# Description
`Bitroot-core` is the reference implementation of the [Counterparty Protocol](https://counterparty.io).

**Note:** for the command-line interface to `bitroot-lib`, see [`bitroot-cli`](https://github.com/BitrootD/Bitroot-cli.git).


# Installation

**WARNING** Master branch should only be used for testing. For production releases uses tagged releases.


# Manual installation

Download the latest [Bitcoin Core](https://github.com/bitcoin/bitcoin/releases) and create
a `bitcoin.conf` file with the following options:

```
rpcuser=bitcoinrpc
rpcpassword=rpc
server=1
txindex=1
rpctimeout=300
zmqpubhashblock=tcp://127.0.0.1:28832
zmqpubhashtx=tcp://127.0.0.1:28832
addresstype=legacy
```
**Note:** you can and should replace the RPC credentials. Remember to use the changed RPC credentials throughout this document.

Download and install latest addrindexrs:
```
$ git clone https://github.com/BitrootD/addrindexrs.git
$ cd addrindexrs
$ cargo check
 -- Setup the appropiate environment variables --
  - ADDRINDEXRS_JSONRPC_IMPORT=1
  - ADDRINDEXRS_TXID_LIMIT=15000
  - ADDRINDEXRS_COOKIE=user:password
  - ADDRINDEXRS_INDEXER_RPC_ADDR=0.0.0.0:8432
  - ADDRINDEXRS_DAEMON_RPC_ADDR=bitcoin:8332
 --
$ cargo build --release
$ cargo run --release
```

You could run the indexd daemon with a process manager like `forever` or `pm2` (recommended).

Then, download and install `Bitroot-core`:

```
$ git clone https://github.com/BitrootD/Bitroot-core.git
$ cd bitroot-lib
$ sudo pip3 install --upgrade -r requirements.txt
$ sudo python3 setup.py install
```

Followed by `Bitroot-cli`:

```
$ git clone https://github.com/BitrootD/Bitroot-cli.git
$ cd Bitroot-cli
$ sudo pip3 install --upgrade -r requirements.txt
$ sudo python3 setup.py install
```

Note on **sudo**: both bitroot-lib and bitroot-server can be installed by non-sudoers. Please refer to external documentation for instructions on using pip without root access and other information related to custom install locations.


Then, launch the daemon via:

```
$ bitroot-server bootstrap
$ bitroot-server --backend-password=rpc start
```

# Basic Usage

## Via command-line

(Requires `Bitroot-cli` to be installed.)

* The first time you run the server, you may bootstrap the local database with:
	`$ bitroot-server bootstrap`

* Start the server with:
	`$ bitroot-server start`

* Check the status of the server with:
	`$ bitroot-client getinfo`

* For additional command-line arguments and options:
	`$ bitroot-server --help`
	`$ bitroot-client --help`

## Via Python

Bare usage from Python is also possible, without installing `Bitroot-cli`:

```
$ python3
>>> from bitrootlib import server
>>> db = server.initialise(<options>)
>>> server.start_all(db)
```

# Configuration and Operation

The paths to the **configuration** files, **log** files and **database** files are printed to the screen when starting the server in ‘verbose’ mode:
	`$ bitroot-server --verbose start`

By default, the **configuration files** are named `server.conf` and `client.conf` and located in the following directories:

* Linux: `~/.config/bitroot/`
* Windows: `%APPDATA%\Bitroot\`

Client and Server log files are named `bitroot.client.[testnet.]log` and `bitroot.server.[testnet.]log`, and located in the following directories:

* Linux: `~/.cache/bitroot/log/`
* Windows: `%APPDATA%\Local\Bitroot\bitroot\Logs`

Counterparty API activity is logged in `server.[testnet.]api.log` and `client.[testnet.]api.log`.

Counterparty database files are by default named `bitroot.[testnet.]db` and located in the following directories:

* Linux: `~/.local/share/bitroot`
* Windows: `%APPDATA%\Roaming\Bitroot\bitroot`

## Configuration File Format

Manual configuration is not necessary for most use cases. "back-end" and "wallet" are used to access Bitcoin server RPC.

A `bitroot-server` configuration file looks like this:

	[Default]
	backend-name = indexd
	backend-user = <user>
	backend-password = <password>
	indexd-connect = localhost
	indexd-port = 8432
	rpc-host = 0.0.0.0
	rpc-user = <rpcuser>
	rpc-password = <rpcpassword>

The ``force`` argument can be used either in the server configuration file or passed at runtime to make the server keep running in the case it loses connectivity with the Internet and falls behind the back-end database. This may be useful for *non-production* Bitroot servers that need to maintain RPC service availability even when the backend or Bitroot server has no Internet connectivity.

A `bitroot-client` configuration file looks like this:

	[Default]
	wallet-name = bitcoincore
	wallet-connect = localhost
	wallet-user = <user>
	wallet-password = <password>
	bitroot-rpc-connect = localhost
	bitroot-rpc-user = <rpcuser>
	bitroot-rpc-password = <password>


# Developer notes

## Versioning

* Major version changes require a full (automatic) rebuild of the database.
* Minor version changes require a(n automatic) database reparse.
* All protocol changes are retroactive on testnet.

## Continuous integration
 - TravisCI is setup to run all tests with 1 command and generate a coverage report and let `python-coveralls` parse and upload it.
   It does runs with `--skiptestbook=all` so it will not do the reparsing of the bootstrap files.
 - CircleCI is setup to split the tests as much as possible to make it easier to read the error reports.
   It also runs the `integration_test.test_book` tests, which reparse the bootstrap files.


# Further Reading

* [Official Project Documentation](http://counterparty.io/docs/)
