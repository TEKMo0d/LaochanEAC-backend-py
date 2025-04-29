from ..utils.kbinxml import toObject, XMLParser
import json

with open('input.xml','r') as file:
    XML_CONTENT = file.read()
    
parserIntools = XMLParser({
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

parsed_xml = parserIntools.parse(XML_CONTENT)

obj = toObject(parsed_xml)

with open('output.json', 'w') as file:
    json.dump(obj, file, indent=2)
