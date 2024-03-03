from .erc20_abi import ERC20_ABI
from web3 import Web3
from ..constants import SYNCSWAP_ROUTER_ADDRESS, USDC_ADDRESS, USDT_ADDRESS

token_name_dict = {"USDC": USDC_ADDRESS,
                   "USDT": USDT_ADDRESS}


class Token:
    """
    This class represents the USDC token and provides methods to interact with its smart contract,
    such as checking allowances, balances, and enabling token swaps via approval transactions.
    """

    def __init__(self, web3, token_address):
        """
        Initializes an instance of the USDC class.

        :param web3: A Web3 instance connected to an Ethereum node.
        :param syncswap_contract: An instance of the SyncSwapContract class.
        :param usdc_address: The address of the USDC token contract (defaults to USDC_ADDRESS).
        """
        self.web3 = web3
        self.token = web3.eth.contract(address=token_address, abi=ERC20_ABI)

    @classmethod
    def from_token_name(cls, web3, token_name):
        if token_name not in token_name_dict:
            raise Exception("Token not recognized")
        return cls(web3, token_name_dict[token_name])

    def allowance(self, address, syncswap_address=SYNCSWAP_ROUTER_ADDRESS):
        """
        Retrieves the amount of USDC tokens that the SyncSwap contract is allowed to spend on behalf of the specified address.

        :param address: The address to check the allowance for.
        :return: The allowance amount.
        """
        allowance = self.token.functions.allowance(address,
                                                   Web3.to_checksum_address(syncswap_address)).call()
        return allowance

    def balance(self, address):
        """
        Retrieves the USDC token balance of the specified address.

        :param address: The address to check the balance for.
        :return: The balance amount.
        """
        return self.token.functions.balanceOf(address).call()

    def allow_swap(self, account, syncswap_address=SYNCSWAP_ROUTER_ADDRESS,
                   amount=115792089237316195423570985008687907853269984665640564039457584007913129639935):
        """
        Approves the SyncSwap contract to spend USDC tokens on behalf of the account up to the specified amount.

        :param syncswap_address: The address of the router contract
        :param account: The account whose tokens are being approved for swap.
        :param amount: The amount of tokens to approve (defaults to the maximum possible).
        :return: A transaction dictionary that can be used to approve the spend.
        """
        function_call = self.token.functions.approve(
            Web3.to_checksum_address(syncswap_address),
            amount
        )

        estimated_gas = function_call.estimate_gas({
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address),
        })

        txn_dict = function_call.build_transaction({
            'gasPrice': self.web3.eth.gas_price,
            'gas': int(estimated_gas * 1.1),
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address),
        })

        return txn_dict
