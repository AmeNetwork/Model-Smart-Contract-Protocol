from abc import ABC, abstractmethod
class AbstractConnector(ABC):
    def __init__(self, rpc, address, account, name):
        self.rpc = rpc
        self.address = address
        self.account = account
        self.name = name

    @abstractmethod
    def call_function(self):
        """
        Call a function of the contract
        :param function_name: The name of the function to call
        :param function_args: The arguments to pass to the function
        :return: The result of the function call
        """
        pass

    @abstractmethod
    def get_functions(self):
        """
        Get all functions of the contract
        :return: A list of function objects
        :example:
        [
            {
                "type": "function",
                "function": {
                    "name": "function_name",
                    "description": "function description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "param1": {
                                "type": "string",
                                "description": "param1 description",
                            },
                        },
                        "required": ["param1"],
                    },
                },
            },
        ]
        """
        pass