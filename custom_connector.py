from mscp.connectors.abstract_connector import AbstractConnector
from mscp.lib import abi_to_openai_type
from web3 import Web3
import json


class CustomConnector(AbstractConnector):
    def __init__(self, rpc, address, account, type="custom_connector"):
        self.rpc = rpc
        self.address = address
        self.account = account
        self.type = type
        self.web3 = Web3(Web3.HTTPProvider(rpc))

        self.abi = [
            {
                "inputs": [],
                "name": "getETHPrice",
                "outputs": [
                        {
                            "internalType": "uint256",
                            "name": "",
                            "type": "uint256"
                        }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_price",
                                "type": "uint256"
                    }
                ],
                "name": "setETHPrice",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        self.contract = self.web3.eth.contract(address=address, abi=self.abi)

    def call_function(self, function):
        args = json.loads(function.arguments)
        if function.name == "getETHPrice":
            result = self.contract.functions.getETHPrice().call()

            return str({
                "eth_price": result
            })
        elif function.name == "setETHPrice":
            tx = self.contract.functions.setETHPrice(args["_price"]).build_transaction(
                {
                    "chainId": self.web3.eth.chain_id,
                    "gas": 200000,
                    "gasPrice": self.web3.to_wei("10", "gwei"),
                    "nonce": self.web3.eth.get_transaction_count(self.account.address),
                }
            )
            signed_tx = self.account.sign_transaction(tx)
            self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return "success"

    def get_functions(self):

        get_eth_price = abi_to_openai_type(
            self.abi, "getETHPrice", "when user want to get eth price")
        set_eth_price = abi_to_openai_type(
            self.abi, "setETHPrice", "set eth price")

        return [get_eth_price, set_eth_price]
