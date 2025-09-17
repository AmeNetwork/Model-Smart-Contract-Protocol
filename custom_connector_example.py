from openai import OpenAI
from eth_account import Account
from mscp import Chat2Web3
from custom_connector import CustomConnector
from dotenv import load_dotenv
import os

load_dotenv()
# Create a connector to connect to the component
custom_connector = CustomConnector(
    "http://localhost:8545",  # RPC of the component network
    "0xE5BA7084738747631baFb38b1226C501784c90c2",  # component address
    Account.from_key(os.getenv("EVM_PRIVATE_KEY")),
)

# Create a Chat2Web3 instance
chat2web3 = Chat2Web3([custom_connector])

# Create a client for OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

# Set up the conversation
messages = [
    {
        "role": "user",
        "content": "get eth price",
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

print(func_msg)

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


