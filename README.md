<div align="center">
  <img src="./mscp_logo.svg" width="60" height="60" />
  <h1>Model Smart Contract Protocol (MSCP)</h1>
  <p>A standard protocol that enables LLM applications to interact with EVM-compatible networks.</p>

![Version](https://img.shields.io/badge/version-0.1.3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Powered by](https://img.shields.io/badge/powered_by-ame_network-8A2BE2)](https://ame.network)

</div>

## Features
**Component as a service**  
AI Agent interacts with the network by operating different components.

**Fast integration**   
Component-based design makes it easier to build workflows and accelerates the development of AI applications.

**Unified interaction**   
Use consistent rules and protocols to standardize the calls to contracts with different functions and ensure the consistency of AI interactions.

**Dynamic expansion**   
AI Agent can add custom onchain components with greater flexibility.

**EVM compatibility**   
It can interact with multiple EVM-compatible network contracts at the same time, and has greater adaptability in handling tasks in complex scenarios.

**Decentralization**   
Access component capabilities without permission, share onchain data, and provide persistent services and information verification.


## Architecture
![MSCP Architecture](./mscp_architecture.png)

### MSCP consists of three parts:

**Component:** This is a smart contract that complies with [ERC-7654](https://eips.ethereum.org/EIPS/eip-7654). 

**Connectors:** This is used to establish a connection with a component and convert its methods into tool functions that can be interacted with by the LLM.  
In addition, it supports customization, you can customize different Connectors according to different smart contracts.


**Chat2Web3:** This is a router that dynamically calls the connector based on the response from the LLM.

## Quick Start
### Install
```shell
pip install mscp
```

### Set up environment variables
Please refer to `.env.example` file, and create a `.env` file with your own settings. You can use two methods to import environment variables.

### Deploy Component Smart Contract

Here is a simple component [example.sol](./contracts/Example.sol) that you can deploy on any network.

### Integrate MSCP into your AI application

```python
from openai import OpenAI
from eth_account import Account
from mscp import Chat2Web3
from mscp.connectors import ERC7654Connector
from dotenv import load_dotenv
import os

load_dotenv()
# Create a connector to connect to the component
component_connector = ERC7654Connector(
    "http://localhost:8545",  # RPC of the component network
    "0x0E2b5cF475D1BAe57C6C41BbDDD3D99ae6Ea59c7",  # component address
    Account.from_key(os.getenv("EVM_PRIVATE_KEY")),
)

# Create a Chat2Web3 instance
chat2web3 = Chat2Web3([component_connector])

# Create a client for OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

# Set up the conversation
messages = [
    {
        "role": "user",
        "content": "What is the user's name and age? 0x8241b5b254e47798E8cD02d13B8eE0C7B5f2a6fA",
    }
]

# Add the chat2web3 to the tools
params = {
    "model": "gpt-3.5-turbo",
    "messages": messages,
    "tools": chat2web3.functions,
}

# Start the conversation
response = client.chat.completions.create(**params)

# Get the function message
func_msg = response.choices[0].message

# fliter out chat2web3 function
if func_msg.tool_calls and chat2web3.has(func_msg.tool_calls[0].function.name):

    # execute the function from llm
    function_result = chat2web3.call(func_msg.tool_calls[0].function)

    messages.extend(
        [
            func_msg,
            {
                "role": "tool",
                "tool_call_id": func_msg.tool_calls[0].id,
                "content": function_result,
            },
        ]
    )

    # Model responds with final answer
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

    print(response.choices[0].message.content)

```

## Integrations
### Integrate MSCP into Aser Agent
Aser is a minimalist, modular, and versatile AI agent framework. You can assemble an agent with just a few lines of code. Learn more about aser agent [here](https://github.com/ame-network/aser-agent).
```python
# Create a Connector instance for the component
component_connector = Connector(
    "http://127.0.0.1:8545",  # RPC URL
    "0x0E2b5cF475D1BAe57C6C41BbDDD3D99ae6Ea59c7",  # component contract address
    Account.from_key(os.getenv("EVM_PRIVATE_KEY"))  # Load account from private key in environment variable
)

# Initialize Chat2Web3 with the component connector
chat2web3 = Chat2Web3([component_connector])

# Create an Agent instance with chat2web3
agent = Agent(name="chat2web3", model="gpt-4o", chat2web3=chat2web3)

# Use the agent to chat and get the user's name and age by passing an address
response = agent.chat("What is the user's name and age?0x8241b5b254e47798E8cD02d13B8eE0C7B5f2a6fA")

# Print the response from the agent
print(response)

```

### Integrate smart contracts through Custom Connector

Developers can customize Connector functions to adapt to different contracts.
Please refer to the following steps:

**1. Depoly Your Contract**.  
Deploy your custom contract. Here is a [CustomConnectorContract.sol](./contracts/CustomConnectorContract.sol) as example that you can deploy directly.   


**2. Implement the Connector**.  
Developers can implement interface abstraction to customize different connectors
```python
from abc import ABC, abstractmethod

class AbstractConnector(ABC):
    def __init__(self, rpc, address, account, type):
        self.rpc = rpc
        self.address = address
        self.account = account
        self.type = type

    @abstractmethod
    def call_function(self, function):
        pass

    @abstractmethod
    def get_functions(self):
        pass
```
You can refer to the [custom_connector](./custom_connector.py).

**3. Add the Connector to Chat2Web3**.  
Add the implemented connector to the Chat2Web3 instance.

```python
chat2web3 = Chat2Web3([custom_connector])
```
You can refer to the [custom_connector_example](./custom_connector.py).

### Integrate ERC8004 Connector
ERC8004 is a standard interface for smart contracts that enables agents to discover and and establish trust through reputation and validation.  

- [ERC8004](https://eips.ethereum.org/EIPS/eip-8004)  
- [ERC8004 Smart Contracts by ChaosChain](https://github.com/ChaosChain/chaoschain-genesis-studio/tree/main/contracts/src) 
- [ERC8004 Identity Connector](./mscp/connectors/erc8004.py)

This example demonstrates agent identity registration
```python
from aser import Agent
from mscp import Chat2Web3
from mscp.connectors.erc8004 import ERC8004IdentityConnector
from eth_account import Account
import os

# Load account from environment variable
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))

# Initialize ERC8004 identity connector with RPC, contract address, and account
identity_connector = ERC8004IdentityConnector(
    "http://127.0.0.1:8545",
    "0x8e0E422Ad7BdAbB4e90Edfdd0424039434e38e42",
    account
)

# Create Chat2Web3 instance with the identity connector
chat2web3 = Chat2Web3([identity_connector])

# Create an Agent instance, specifying name, model, and chat2web3
agent = Agent(name="chat2web3", model="gpt-4o", chat2web3=chat2web3)

# Send a chat request to create a new agent with domain and address info
response = agent.chat(
    f"""
    create a newAgent
    agentDomain: http://www.ame.network
    agentAddress: {account.address}
    """
)

# Print the response from the agent
print(response)

```





