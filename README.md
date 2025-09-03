<div align="center">
  <img src="./mscp_logo.svg" width="60" height="60" />
  <h1>Model Smart Contract Protocol (MSCP)</h1>
  <p>A standard protocol that enables LLM applications to interact with EVM-compatible networks.</p>

![Version](https://img.shields.io/badge/version-0.1.1-blue.svg)
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

**Component:** This is an on-chain component that complies with [EIP-7654](https://eips.ethereum.org/EIPS/eip-7654). It is used to implement the specific functions of the contract and provide custom services.

**Connector:** This is a method and specification for parsing Components and processing contract component requests.

**Chat2Web3:** This is an interoperator, which is used to automatically convert the interaction methods of contract components into tool functions that LLM can call. ​

## Quick Start
### Install
```shell
pip3 install mscp
```

### Set up environment variables
Please refer to `.env.example` file, and create a `.env` file with your own settings. You can use two methods to import environment variables.

### Deploy Component Smart Contract

Here is a simple component [example.sol](./component/Example.sol) that you can deploy on any network.

### Integrate MSCP into your AI application

```python
from openai import OpenAI
from eth_account import Account
from mscp import Connector, Chat2Web3
from dotenv import load_dotenv
import os

load_dotenv()
# Create a connector to connect to the component
component_connector = Connector(
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

### Use MSCP in the aser agent
```python

component_connector = Connector(
    "http://127.0.0.1:8545",
    "0x0E2b5cF475D1BAe57C6C41BbDDD3D99ae6Ea59c7",  
    Account.from_key(os.getenv("EVM_PRIVATE_KEY")) 
)
chat2web3 = Chat2Web3([component_connector])
agent=Agent(name="chat2web3",model="gpt-4o",chat2web3=chat2web3)
response = agent.chat("What is the user's name and age?0x8241b5b254e47798E8cD02d13B8eE0C7B5f2a6fA")

print(response)

```



