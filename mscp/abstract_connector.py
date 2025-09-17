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