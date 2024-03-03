# SyncSwapClient


SyncSwapClient is a Python library designed to facilitate interactions with the SyncSwap decentralized exchange (DEX) on the Ethereum blockchain. It abstracts the complexities of direct smart contract interactions, allowing users to easily execute token swaps, manage allowances, and handle transaction preparations.

# Features
Token swap execution via the SyncSwap DEX router.
Automatic gas estimation and allowance verification.
Support for ERC-20 token swaps.
Easy integration with existing Python projects


# Installation
To install SyncSwapClient, you can use pip.

```bash
 pip install git+https://github.com/fedllanes/syncswapclient.git
```

Quick Start
Here's how to start using it. More examples can be seen in the Example_usage.ipybn jupyter notebook.

```python
from web3 import Web3
from eth_account import Account
from syncswap import SyncSwapContract
from syncswap.constants import ZKSYNC_PROVIDER_MAIN, SYNCSWAP_ROUTER_ADDRESS
from syncswap.tokenpairs import ETH2USDC, USDC2ETH

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(ZKSYNC_PROVIDER_MAIN))

# Securely load your private key
private_key = "your_private_key_here"

# Generate your account instance
account = Account.from_key(private_key)

# Initialize the SyncSwapContract
contract = SyncSwapContract(web3, SYNCSWAP_ROUTER_ADDRESS)

# Define the amount to swap (in Wei)
amount_to_swap = 10000000000000

# Perform the token swap
tx_hash = contract.swap_tokens(account, ETH2USDC, amount_to_swap, gas_multiplier=1.1)

# Wait for the transaction to be mined
web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Swap transaction successful: {tx_hash.hex()}")
```
License
SyncSwapClient is released under the MIT License. See the LICENSE file for more details.
