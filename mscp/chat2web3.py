from eth_abi import encode, decode
from mscp.connector import Connector
from mscp.lib import parse_method_to_function


class Chat2Web3:
    def __init__(self, connectors):
        self.functions = []
        self.methods = []
        self.connectors = {}
        self.support_connector = ["eip7654"]
        for connector in connectors:
            self.add(connector)

    def add(self, connector):
        if connector.type not in self.support_connector:
            return None
        else:
            connector_id = len(self.connectors)
            self.connectors[connector_id] = {}
            self.connectors[connector_id]["connector"] = connector
            functions = connector.get_functions()
            self.functions.extend(functions)
            self.connectors[connector_id]["functions"] = functions
            return connector_id

    def get_connector_by_id(self, connector_id):
        return self.connectors[connector_id]["connector"]

    def get_connector_by_function_name(self, function_name):
        for connector_index in self.connectors:
            for function in self.connectors[connector_index]["functions"]:
                if function["function"]["name"] == function_name:
                    return self.connectors[connector_index]["connector"]
        return None

    def has(self, function_name):
        return any(item["function"]["name"] == function_name for item in self.functions)

    def call(self, function):

        connector = self.get_connector_by_function_name(function.name)

        response = connector.call_function(function)

        return response
