import requests
from typing import Dict, Any, TypeVar, Generic, Optional, Union

from utils.types import AcRelayInfo
from utils.kbinxml import fromKBinXml, toKBinXml, toObject
from utils.kxml_value import Serializable
from utils.lz77 import Lz77
from utils.laochan_id import token_to_card_number
from utils.config import *

PCB_ID = '1A0C1A0C1A0C1A0C1A0C'

T = TypeVar('T')
LZ77 = Lz77()

async def requestEa3(info: AcRelayInfo, model: str, token: str, ea3Url: str = 'http://maomani.cn:573/') -> Dict[str, Union[int, Serializable]]:

    if config.is_dev:
        print('ea3 call:')

    request = toKBinXml('call', {
        info.module: {
            '$method': info.method,
            '$model': model,
            '$cardid': token_to_card_number(token),
            '$srcid': PCB_ID,
            **info.request,
        },
    }, 'UTF-8', config.is_dev)

    compressed = LZ77.compress(request.data)
    
    headers = {
        'X-Compress': 'lz77',
    }
    
    response = requests.post(
        f"{ea3Url}/?model={model}&f={info.module}.{info.method}",
        data=compressed,
        headers=headers
    )
    
    raw = bytearray(response.content)
    if response.headers.get('x-compress') == 'lz77':
        result = bytearray(LZ77.decompress(raw))
    else:
        result = raw

    if config.is_dev:
        print('ea3 response:')

    response_data = fromKBinXml(result, config.is_dev)
    
    status = int(response_data['response'].get(info.module, {}).get('$status', '0'))
    
    return {
        'status': status,
        'response': response_data['response'],
    }

async def requestEa3Typed(info: AcRelayInfo, model: str, token: str, ea3Url: Optional[str] = None) -> T:
    result = await requestEa3(info, model, token, ea3Url)
    return toObject(result['response'])