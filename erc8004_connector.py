from mscp.abstract_connector import AbstractConnector
from mscp.lib import abi_to_openai_type
from web3 import Web3
from web3.exceptions import ContractLogicError
import json


class ERC8004Connector(AbstractConnector):
    def __init__(self, rpc, address, account, type="erc8004_connector"):
        self.rpc = rpc
        self.address = address
        self.account = account
        self.type = type
        self.web3 = Web3(Web3.HTTPProvider(rpc))

        self.abi = """ [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "AddressAlreadyRegistered",
		"type": "error"
	},
	{
		"inputs": [],
		"name": "AgentNotFound",
		"type": "error"
	},
	{
		"inputs": [],
		"name": "DomainAlreadyRegistered",
		"type": "error"
	},
	{
		"inputs": [],
		"name": "InvalidAddress",
		"type": "error"
	},
	{
		"inputs": [],
		"name": "InvalidDomain",
		"type": "error"
	},
	{
		"inputs": [],
		"name": "UnauthorizedRegistration",
		"type": "error"
	},
	{
		"inputs": [],
		"name": "UnauthorizedUpdate",
		"type": "error"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "agentId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "agentDomain",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "agentAddress",
				"type": "address"
			}
		],
		"name": "AgentRegistered",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "agentId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "agentDomain",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "agentAddress",
				"type": "address"
			}
		],
		"name": "AgentUpdated",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "VERSION",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "agentId",
				"type": "uint256"
			}
		],
		"name": "agentExists",
		"outputs": [
			{
				"internalType": "bool",
				"name": "exists",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "agentId",
				"type": "uint256"
			}
		],
		"name": "getAgent",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "agentId",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "agentDomain",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "agentAddress",
						"type": "address"
					}
				],
				"internalType": "struct IIdentityRegistry.AgentInfo",
				"name": "agentInfo",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAgentCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "count",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "agentDomain",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "agentAddress",
				"type": "address"
			}
		],
		"name": "newAgent",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "agentId",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "agentAddress",
				"type": "address"
			}
		],
		"name": "resolveByAddress",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "agentId",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "agentDomain",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "agentAddress",
						"type": "address"
					}
				],
				"internalType": "struct IIdentityRegistry.AgentInfo",
				"name": "agentInfo",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "agentDomain",
				"type": "string"
			}
		],
		"name": "resolveByDomain",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "agentId",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "agentDomain",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "agentAddress",
						"type": "address"
					}
				],
				"internalType": "struct IIdentityRegistry.AgentInfo",
				"name": "agentInfo",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "agentId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "newAgentDomain",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "newAgentAddress",
				"type": "address"
			}
		],
		"name": "updateAgent",
		"outputs": [
			{
				"internalType": "bool",
				"name": "success",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]"""
        self.contract = self.web3.eth.contract(address=address, abi=self.abi)

    def call_function(self, function):
        args = json.loads(function.arguments)
        if function.name == "newAgent":
            try:
                result = self.contract.functions.resolveByAddress(args["agentAddress"]).call()

                return str(result)
            except ContractLogicError as e:
                register_info = self.send_transaction(function.name, args, "AgentRegistered")
                return register_info
        elif function.name == "resolveByAddress":
            try:
                result = self.contract.functions.resolveByAddress(args["agentAddress"]).call()
                return str(result)
            except ContractLogicError as e:
                return str("You have not registered this agent")

    def get_functions(self):

        new_agent = abi_to_openai_type(
            self.abi, "newAgent", "when user want to create a new agent")
        get_agent = abi_to_openai_type(self.abi, "resolveByAddress", "get agent info")
        return [new_agent, get_agent]

    def send_transaction(self, function_name, function_args, event_name=None,value=0):

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
            event=dict(event_list[0]["args"])
            return json.dumps(event)
        else:
            return txn_hash


