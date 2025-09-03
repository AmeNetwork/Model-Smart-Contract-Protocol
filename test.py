from openai import OpenAI
from eth_account import Account
from mscp import Connector, Chat2Web3
from dotenv import load_dotenv
import os

load_dotenv()

component_connector = Connector(
    "http://localhost:8545",
    "0x0E2b5cF475D1BAe57C6C41BbDDD3D99ae6Ea59c7",
    Account.from_key(os.getenv("EVM_PRIVATE_KEY")),
)

component_connector.attach_value("createUser","user need pay money")

functions=component_connector.get_functions()
print(functions)
# chat2web3 = Chat2Web3()
# chat2web3.add(component)
# is_has=chat2web3.has("getUser")
# print(is_has)
# connector = chat2web3.get_connector_by_function_name("getUser")
# print(connector.type)
