from openai import OpenAI
from eth_account import Account
from mscp import Connector, Chat2Web3
from dotenv import load_dotenv
import os

load_dotenv()
# Create a connector to connect to the component
component = Connector(
    "http://127.0.0.1:8545",  # RPC of the component network
    "0x5b38CE75E7F755A2F6Fb4915C8A52B2d87Fd8ea0",  # component address
)

# Get the methods of the component
methods = component.get_methods()

# Import the private key from the environment variable
account = Account.from_key(os.getenv("EVM_PRIVATE_KEY"))

# Create a Chat2Web3 instance
chat2web3 = Chat2Web3(account)

# Add methods to chat2web3
chat2web3.add(
    name="createContent",
    prompt="When a user wants to create a content on chainfeed, call this function",
    method=methods["createContent"],  
)
chat2web3.add(
    name="getRecentContent",
    prompt="When a user wants to get the recent content on chainfeed, call this function",
    method=methods["getRecentContent"],  
)

# Create a client for OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

# Set up the conversation
messages = [
    {
        "role": "user",
        "content": "get recent content on chainfeed",
    }
]

# Add the chat2web3 to the tools
params = {"messages": messages, "tools": chat2web3.functions, "model": "gpt-3.5-turbo"}

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
