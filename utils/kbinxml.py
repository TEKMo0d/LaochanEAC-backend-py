import json
import re
from typing import Any, Dict, List, Union, Optional
from datetime import datetime
import binascii
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr
import kbinxml


from kxml_value import Serializable, KValueG, v

class XMLParser:
    def __init__(self, config=None):
        self.config = {
            "ignoreAttributes": False,
            "parseAttributeValue": False,
            "attributeNamePrefix": "$",
            "removeNSPrefix": True,
            "textNodeName": "__value",
            "numberParseOptions": {
                "hex": False,
                "leadingZeros": False,
                "eNotation": False,
                "skipLike": r".*",
            }
        }
    def parse(self, xml_string):
        try:
            root = ET.fromstring(xml_string)
            clean_tag = self._clean_tag(root.tag)
            result = {
                clean_tag: self._process_element(root)
            }
            
            return self._normalize_result(result)
        except Exception as e:
            raise Exception(f"XML解析错误: {str(e)}")

def parseValue(node: Dict[str, Any]) -> Any:
    is_array = "__count" in node
    node_type = node.get("__type")
    node_value = node.get("__value", "")

    if node_type in ["s8", "u8", "s16", "u16", "s32", "u32", "s64", "u64"]:
        if is_array:
            return [int(v) for v in node_value.split()]
        return int(node_value)

    if node_type in ["float", "double"]:
        if is_array:
            return [float(v) for v in node_value.split()]
        return float(node_value)

    if node_type in ["b", "bool"]:
        return bool(int(node_value))

    if node_type in ["bin", "binary"]:
        return binascii.unhexlify(node_value)

    if node_type in ["ip4", "str", "string"]:
        return node_value

    if node_type == "time":
        return datetime.fromtimestamp(int(node_value))

    return {
        "type": node_type,
        "value": node_value
    }

def toObject(node: Union[Dict[str, Any], List[Any], str]) -> Any:
    
    if isinstance(node, list):
        return [toObject(v) for v in node]

    if isinstance(node, str):
        return {}

    if "__type" in node:
        return parseValue(node)

    obj = {}

    for key, value in node.items():
        if key == "?xml":
            continue

        if key.startswith("$"):
            obj[key[1:]] = value
            continue

        obj[key] = toObject(value)

    return obj

def fromKBinXml(kbinxml_data: bytes, dump_xml: bool = False) -> Dict[str, Any]:
    custom_parser = XMLParser({
        "ignoreAttributes": False,
        "parseAttributeValue": False,
        "attributeNamePrefix": "$",
        "removeNSPrefix": True,
        "textNodeName": "__value",
        "numberParseOptions": {
            "hex": False,
            "leadingZeros": False,
            "eNotation": False,
            "skipLike": r".*"
        }
    })
    
    xml_string = kbinxml.decode(kbinxml_data)
    
    if dump_xml:
        print(xml_string)
        
    return custom_parser.parse(xml_string)

def serializeValue(value: Any, type_name: str) -> str:
    if type_name in ["s8", "u8", "s16", "u16", "s32", "u32", "s64", "u64", "float", "double"]:
        return str(value)

    if type_name in ["b", "bool"]:
        return "1" if value else "0"

    if type_name in ["bin", "binary"]:
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("binary值必须是bytes或bytearray类型")
        return binascii.hexlify(value).decode('ascii')

    if type_name in ["ip4"]:
        return value

    if type_name in ["str", "string"]:
        return escape(value)

    if type_name == "time":
        if isinstance(value, datetime):
            return str(int(value.timestamp()))
        if isinstance(value, (int, float)):
            return str(int(value))
        raise TypeError("time值必须是datetime或数字类型")

    raise ValueError(f"不支持的类型 {type_name}")

def serializeObject(obj: Dict[str, Any], name: str, line_prefix: str = "") -> str:
    output = f"{line_prefix}<{name}"

    entries = list(obj.items())
    attrs = [(k[1:], v) for k, v in entries if k.startswith("$")]

    value_entry = next(((k, v) for k, v in entries if k == "__value"), None)

    if value_entry and isinstance(value_entry[1], list):
        attrs.append(("__count", len(value_entry[1])))

    if value_entry and isinstance(value_entry[1], (bytes, bytearray)):
        attrs.append(("__size", len(value_entry[1])))

    attrs.sort(key=lambda x: x[0], reverse=True)

    for attr_name, attr_value in attrs:
        if attr_value is None:
            continue
        output += f' {attr_name}={quoteattr(str(attr_value))}'

    output += ">"

    if value_entry:
        if value_entry[1] is None:
            return ""

        type_attr = next((attr for attr in attrs if attr[0] == "__type"), None)

        if not type_attr:
            raise ValueError(f"{name}中的值没有类型")

        values = value_entry[1] if isinstance(value_entry[1], list) else [value_entry[1]]
        output += " ".join(serializeObject(v, type_attr[1]) for v in values)
    else:
        elements = [(k, v) for k, v in entries if not k.startswith("$")]
        elements.sort(key=lambda x: x[0], reverse=True)

        if elements:
            output += "\n"

            for elem_name, elem_value in elements:
                if isinstance(elem_value, list):
                    for item in elem_value:
                        output += serializeObject(item, elem_name, line_prefix + "  ")
                    continue

                output += serializeObject(elem_value, elem_name, line_prefix + "  ")

            output += line_prefix

    return output + f"</{name}>\n"

def toKBinXml(top_name: str, obj: Serializable, encoding: str = "UTF-8", 
              dump_xml: bool = False) -> bytes:
    xml_str = f'<?xml version="1.0" encoding="{encoding}"?>{serializeObject(obj, top_name)}'

    if dump_xml:
        print(xml_str)

    return kbinxml.encode(xml_str)