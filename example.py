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
