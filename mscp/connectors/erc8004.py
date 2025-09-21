from mscp.connectors.abstract_connector import AbstractConnector
from mscp.lib import abi_to_openai_type
from web3 import Web3
from web3.exceptions import ContractLogicError
import json
import os


class ERC8004IdentityConnector(AbstractConnector):
    def __init__(self, rpc, address, account, name="erc8004"):
        self.rpc = rpc
        self.address = address
        self.account = account
        self.name = name
        self.web3 = Web3(Web3.HTTPProvider(rpc))

        # Get the directory of this module and construct the ABI file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        abi_path = os.path.join(current_dir, "abis", "erc8004_identity.json")
        with open(abi_path, "r") as f:
            self.abi = json.load(f)
        self.contract = self.web3.eth.contract(address=address, abi=self.abi)

    def call_function(self, function):
        args = json.loads(function.arguments)
        if function.name == "newAgent":
            try:
                register_info = self.contract.functions.resolveByAddress(
                    args["agentAddress"]).call()

                response = {
                    "id": register_info[0],
                    "domain": register_info[1],
                    "address": register_info[2]
                }

                return json.dumps(response)
            except ContractLogicError as e:
                register_info = self.send_transaction(
                    function.name, args, "AgentRegistered")
                return register_info
        elif function.name == "resolveByAddress":
            try:
                register_info = self.contract.functions.resolveByAddress(
                    args["agentAddress"]).call()

                response = {
                    "id": register_info[0],
                    "domain": register_info[1],
                    "address": register_info[2]
                }
                return json.dumps(response)
            except ContractLogicError as e:
                return str("You have not registered this agent")

    def get_functions(self):

        new_agent = abi_to_openai_type(
            self.abi, "newAgent", f"""when user want to create a new agent""")
        get_agent = abi_to_openai_type(
            self.abi, "resolveByAddress", f"""when user want to get agent info""")
        return [new_agent, get_agent]

    def send_transaction(self, function_name, function_args, event_name=None, value=0):

        func = getattr(self.contract.functions, function_name)
        build_args = {
            "from": self.account.address,
            "nonce": self.web3.eth.get_transaction_count(self.account.address),
            "value": value,
        }
        estimated_tx = func(**function_args).build_transaction(build_args)
        estimated_gas = self.web3.eth.estimate_gas(estimated_tx)
        gasPrice = self.web3.eth.gas_price
        txn_args = {
            "from": self.account.address,
            "nonce": self.web3.eth.get_transaction_count(self.account.address),
            "gasPrice": gasPrice,
            "gas": estimated_gas,
            "value": value,
        }
        txn = func(**function_args).build_transaction(txn_args)
        signed_txn = self.account.sign_transaction(txn)
        txn_hash = self.web3.eth.send_raw_transaction(
            signed_txn.raw_transaction
        ).hex()
        receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        if event_name:
            event_cls = getattr(self.contract.events, event_name)
            event_list = event_cls().process_receipt(receipt)
            event = dict(event_list[0]["args"])
            return json.dumps(event)
        else:
            return txn_hash
