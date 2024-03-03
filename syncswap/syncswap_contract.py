from .syncswap_abi import SYNCSWAP_ROUTER_ABI
from .constants import wETHAddress, ZERO_ADDRESS
from eth_abi import encode
import time


class SyncSwapContract:
    """
    A class to manage and execute interactions with the SyncSwap smart contract on the Ethereum blockchain.
    It provides functionality to perform token swaps through the SyncSwap decentralized exchange (DEX) router,
    handling all necessary preparations such as gas estimation, allowance verification, and transaction signing.

    Attributes:
        abi (list): The Application Binary Interface (ABI) of the SyncSwap router contract.
        web3 (Web3): An instance of the Web3 class for interacting with the Ethereum blockchain.
        contract (web3.eth.Contract): The contract object instantiated with the SyncSwap router's address and ABI.

    Methods:
        __init__(self, web3, syncswap_router_address): Initializes a new SyncSwapContract instance.
        swap_tokens(self, account, token_pair, amount, withdraw_mode=None, gas_multiplier=None): Executes a token swap operation on the blockchain.
        _verify_allowance(self, token_pair, account, amount): Internal method to ensure the swapping account has sufficient allowance for the swap.
        _estimate_gas(self, function_call, account, amount): Estimates the gas required for a given transaction.
        _build_swap_paths(self, from_address, signer_address, withdrawMode, token_pair, amount): Constructs the data needed for executing a swap through the SyncSwap contract.

    Usage:
        This class is intended to be used in applications that require interaction with the SyncSwap DEX on ZKSYNC era,
        facilitating token swaps by abstracting away the complexities of direct blockchain interaction.
    """

    def __init__(self, web3, syncswap_router_address):
        """
        Initializes the SyncSwapContract instance.

        :param web3: A Web3 instance connected to an Ethereum node.
        :param syncswap_router_address: The address of the SyncSwap router contract.
        """
        self.abi = SYNCSWAP_ROUTER_ABI
        self.web3 = web3
        self.contract = web3.eth.contract(
            address=web3.to_checksum_address(syncswap_router_address),
            abi=self.abi,
        )

    def swap_tokens(self, account, token_pair, amount, withdraw_mode=None, gas_multiplier=None):
        """
        Executes a token swap operation.

        :param account: The account performing the swap.
        :param token_pair: a TokenPair instance containing the from and to token information.
        :param amount: The amount of tokens to swap.
        :param withdraw_mode: The type of withdrawal, 1 for Eth, 2 for weth
        :param gas_multiplier: Multiplier for gas estimation, uses estimated gas if None.
        :return: Transaction hash of the swap operation.
        """
        signer_address = account.address
        if withdraw_mode is None:
            withdraw_mode = 1 if token_pair.to_token_name == "ETH" else 2

        # Let's verify we can move that token
        self._verify_allowance(token_pair, account, amount)
        paths = self._build_swap_paths(token_pair.from_token, signer_address, withdraw_mode, token_pair, amount)

        deadline = int(time.time()) + 600  # 10 minutes from now
        function_call = self.contract.functions.swap(
            paths,
            0,
            deadline
        )

        gas_to_use = self._estimate_gas(function_call, account, amount)
        if isinstance(gas_multiplier, (int, float)):
            gas_to_use = int(gas_to_use * gas_multiplier)

        txn_dict = function_call.build_transaction({
            'from': account.address,
            'value': amount,
            'gas': gas_to_use,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(account.address),
        })
        signed_txn = self.web3.eth.account.sign_transaction(txn_dict, account.key.hex())
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash

    def _verify_allowance(self, token_pair, account, amount):
        """Verifies if the allowance is sufficient for the swap; requests increase if not."""
        if token_pair.from_token_name != "ETH":
            # For non eth tokens, we need to be authorized
            if token_pair.web3 is None:
                token_pair.set_web3(self.web3)

            token = token_pair.from_token_instance

            if token.allowance(account.address) < amount:
                token.allow_swap(account)

    def _estimate_gas(self, function_call, account, amount):
        """Estimates the gas required for the transaction."""
        estimated_gas = function_call.estimate_gas({
            'from': self.web3.to_checksum_address(account.address),
            'value': amount
        })
        return estimated_gas

    @staticmethod
    def _build_swap_paths(from_address, signer_address, withdrawMode, token_pair, amount):
        """Constructs the paths argument for the swap function."""
        swap_data = encode(
            ["address", "address", "uint8"],
            [from_address, signer_address, withdrawMode]
        )

        steps = [token_pair.token_pair_address,  # this is the pair address
                 "",  # this will be replaced with the encoded data
                 ZERO_ADDRESS,  # zero address
                 b"",
                 True]
        steps[1] = swap_data

        paths = [(
            [
                tuple(steps),
            ],
            from_address if from_address != wETHAddress else ZERO_ADDRESS,
            amount
        )]
        return paths
