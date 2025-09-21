import string
import json


def solidity_to_openai_type(solidity_type):
    base_type = solidity_type.rstrip("[]")
    is_array = solidity_type.endswith("[]")

    if base_type == "bool":
        return "array" if is_array else "boolean"

    if base_type.startswith(("int", "uint")):
        return "array" if is_array else "integer"

    if base_type == "address":
        return "array" if is_array else "string"

    if base_type.startswith("bytes") or base_type == "string":
        return "array" if is_array else "string"

    if "[" in base_type and "]" in base_type:
        return "array"

    if base_type.startswith("mapping") or base_type in ["struct", "enum"]:
        return "object"

    return "string"


def parse_method_to_function(methods):
    functions = []
    for method in methods:
        properties = {}
        for index in range(len(method["req"])):
            properties[string.ascii_letters[index]] = {}
            properties[string.ascii_letters[index]]["type"] = solidity_to_openai_type(
                method["req"][index]
            )
        function = {
            "type": "function",
            "function": {
                "name": method["name"],
                "description": method["instruction"],
                "parameters": {"type": "object", "properties": properties},
            },
        }
        functions.append(function)
    return functions


def get_data_types(index):
    types = [
        "bool",
        "int8",
        "int16",
        "int24",
        "int32",
        "int40",
        "int48",
        "int56",
        "int64",
        "int72",
        "int80",
        "int88",
        "int96",
        "int104",
        "int112",
        "int120",
        "int128",
        "int136",
        "int144",
        "int152",
        "int160",
        "int168",
        "int176",
        "int184",
        "int192",
        "int200",
        "int208",
        "int216",
        "int224",
        "int232",
        "int240",
        "int248",
        "int256",
        "uint8",
        "uint16",
        "uint24",
        "uint32",
        "uint40",
        "uint48",
        "uint56",
        "uint64",
        "uint72",
        "uint80",
        "uint88",
        "uint96",
        "uint104",
        "uint112",
        "uint120",
        "uint128",
        "uint136",
        "uint144",
        "uint152",
        "uint160",
        "uint168",
        "uint176",
        "uint184",
        "uint192",
        "uint200",
        "uint208",
        "uint216",
        "uint224",
        "uint232",
        "uint240",
        "uint248",
        "uint256",
        "address",
        "bytes1",
        "bytes2",
        "bytes3",
        "bytes4",
        "bytes5",
        "bytes6",
        "bytes7",
        "bytes8",
        "bytes9",
        "bytes10",
        "bytes11",
        "bytes12",
        "bytes13",
        "bytes14",
        "bytes15",
        "bytes16",
        "bytes17",
        "bytes18",
        "bytes19",
        "bytes20",
        "bytes21",
        "bytes22",
        "bytes23",
        "bytes24",
        "bytes25",
        "bytes26",
        "bytes27",
        "bytes28",
        "bytes29",
        "bytes30",
        "bytes31",
        "bytes32",
        "bytes",
        "string",
        "int8[]",
        "int16[]",
        "int24[]",
        "int32[]",
        "int40[]",
        "int48[]",
        "int56[]",
        "int64[]",
        "int72[]",
        "int80[]",
        "int88[]",
        "int96[]",
        "int104[]",
        "int112[]",
        "int120[]",
        "int128[]",
        "int136[]",
        "int144[]",
        "int152[]",
        "int160[]",
        "int168[]",
        "int176[]",
        "int184[]",
        "int192[]",
        "int200[]",
        "int208[]",
        "int216[]",
        "int224[]",
        "int232[]",
        "int240[]",
        "int248[]",
        "int256[]",
        "uint8[]",
        "uint16[]",
        "uint24[]",
        "uint32[]",
        "uint40[]",
        "uint48[]",
        "uint56[]",
        "uint64[]",
        "uint72[]",
        "uint80[]",
        "uint88[]",
        "uint96[]",
        "uint104[]",
        "uint112[]",
        "uint120[]",
        "uint128[]",
        "uint136[]",
        "uint144[]",
        "uint152[]",
        "uint160[]",
        "uint168[]",
        "uint176[]",
        "uint184[]",
        "uint192[]",
        "uint200[]",
        "uint208[]",
        "uint216[]",
        "uint224[]",
        "uint232[]",
        "uint240[]",
        "uint248[]",
        "uint256[]",
        "address[]",
        "bytes1[]",
        "bytes2[]",
        "bytes3[]",
        "bytes4[]",
        "bytes5[]",
        "bytes6[]",
        "bytes7[]",
        "bytes8[]",
        "bytes9[]",
        "bytes10[]",
        "bytes11[]",
        "bytes12[]",
        "bytes13[]",
        "bytes14[]",
        "bytes15[]",
        "bytes16[]",
        "bytes17[]",
        "bytes18[]",
        "bytes19[]",
        "bytes20[]",
        "bytes21[]",
        "bytes22[]",
        "bytes23[]",
        "bytes24[]",
        "bytes25[]",
        "bytes26[]",
        "bytes27[]",
        "bytes28[]",
        "bytes29[]",
        "bytes30[]",
        "bytes31[]",
        "bytes32[]",
        "bytes[]",
        "string[]",
    ]
    return types[index]


def abi_to_openai_type(abi: str, abi_function_name: str, description: str):

    try:

        abi_data = abi

        target_function = None
        for item in abi_data:
            if item.get("type") == "function" and item.get("name") == abi_function_name:
                target_function = item
                break

        if not target_function:
            raise ValueError(f"Function '{abi_function_name}' not found in ABI")

        properties = {}
        required = []

        for input_param in target_function.get("inputs", []):
            param_name = input_param["name"]
            param_type = input_param["type"]

            json_type, json_format = solidity_to_json_type(param_type)

            param_schema = {"type": json_type}
            if json_format:
                param_schema["format"] = json_format

            param_schema["description"] = f"Parameter {param_name} of type {param_type}"

            properties[param_name] = param_schema
            required.append(param_name)

        tool_function = {
            "type": "function",
            "function": {
                "name": abi_function_name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }

        return tool_function

    except json.JSONDecodeError:
        raise ValueError("Invalid ABI JSON format")
    except Exception as e:
        raise ValueError(f"Error processing ABI: {str(e)}")


def solidity_to_json_type(solidity_type: str):

    type_mapping = {
        "bool": ("boolean", None),
        "string": ("string", None),
        "address": ("string", "address"),
        "bytes": ("string", "bytes"),
        "uint8": ("integer", None),
        "uint16": ("integer", None),
        "uint32": ("integer", None),
        "uint64": ("integer", None),
        "uint128": ("integer", None),
        "uint256": ("integer", None),
        "int8": ("integer", None),
        "int16": ("integer", None),
        "int32": ("integer", None),
        "int64": ("integer", None),
        "int128": ("integer", None),
        "int256": ("integer", None),
    }

    if solidity_type.endswith("[]"):
        base_type = solidity_type[:-2]
        if base_type in type_mapping:
            return ("array", f"items:{type_mapping[base_type][0]}")
        else:
            return ("array", "items:string")

    if "[" in solidity_type and "]" in solidity_type:
        base_type = solidity_type.split("[")[0]
        if base_type in type_mapping:
            return ("array", f"items:{type_mapping[base_type][0]}")
        else:
            return ("array", "items:string")

    if solidity_type in type_mapping:
        return type_mapping[solidity_type]

    return ("string", None)
