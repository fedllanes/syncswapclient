from web3 import Web3

from .constants import wETHAddress, USDC_ADDRESS, USDT_ADDRESS
from .tokens import Token


class TokenPairs:
    """
    A class to represent a pair of tradable tokens within a blockchain ecosystem.

    Attributes:
        from_token (str): The address of the token to trade from.
        to_token (str): The address of the token to trade to.
        token_pair_address (str): The blockchain address of the token pair's smart contract.
        pair_name (str): A descriptive name for the token pair, formatted as 'TOKEN1toTOKEN2'.
        from_token_name (str): Extracted name of the `from_token` for easier reference.
        to_token_name (str): Extracted name of the `to_token` for easier reference.
        web3 (Web3): An instance of the Web3 class to interact with the Ethereum blockchain.
        from_token_instance (Token): An instance of the `Token` class for the `from_token`.
        to_token_instance (Token): An instance of the `Token` class for the `to_token`.

    Methods:
        __init__(self, from_token, to_token, token_pair_address, pair_name):
            Initializes the TokenPairs class with token details and pair information.

        set_web3(self, web3):
            Sets the Web3 instance for interacting with the blockchain and initializes token instances.

        __str__(self):
            Returns a string representation of the token pair, specifically the `pair_name`.
    """
    def __init__(self, from_token, to_token, token_pair_address, pair_name):
        """
        Constructs all the necessary attributes for the TokenPairs object.

        Parameters:
            from_token (str): The address of the token to trade from.
            to_token (str): The address of the token to trade to.
            token_pair_address (str): The blockchain address of the token pair's smart contract.
            pair_name (str): A descriptive name for the token pair, formatted as 'TOKEN1toTOKEN2'.
        """
        self.from_token = from_token
        self.to_token = to_token
        self.token_pair_address = token_pair_address
        self.pair_name = pair_name
        self.from_token_name, self.to_token_name = pair_name.split("2")
        self.web3 = None
        self.from_token_instance = None
        self.to_token_instance = None

    def set_web3(self, web3):
        """
        Sets the Web3 instance for blockchain interaction and initializes instances of the Token class for both tokens in the pair.

        Parameters:
            web3 (Web3): An instance of the Web3 class.
        """
        self.web3 = web3
        self.from_token_instance = Token(web3, Web3.to_checksum_address(self.from_token))
        self.to_token_instance = Token(web3, Web3.to_checksum_address(self.to_token))

    def __str__(self):
        return self.pair_name


ETH2USDC = TokenPairs(wETHAddress, USDC_ADDRESS, "0x80115c708E12eDd42E504c1cD52Aea96C547c05c", "ETH2USDC")
USDC2ETH = TokenPairs(USDC_ADDRESS, wETHAddress, "0x80115c708E12eDd42E504c1cD52Aea96C547c05c", "USDC2ETH")
USDC2USDT = TokenPairs(USDC_ADDRESS, USDT_ADDRESS, "0x0E595bfcAfb552F83E25d24e8a383F88c1Ab48A4", "USDC2USDT")
USDT2USDC = TokenPairs(USDT_ADDRESS, USDC_ADDRESS, "0x0E595bfcAfb552F83E25d24e8a383F88c1Ab48A4", "USDT2USDC")
