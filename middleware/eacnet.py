from typing import Dict, Any, Optional
import base64
from utils.lz77 import Lz77
from utils.kbinxml import fromKBinXml, toObject

async def eacnet(ctx, next):
    body = ctx.request.body
    
    if not body or not hasattr(body, 'request'):
        return await next()
    
    request = body.request
    
    if not request:
        return await next()
    
    modified_request = request.replace(' ', '+').replace('-', '+').replace('_', '/') + '==='
    buffer = base64.b64decode(modified_request)
    
    decoded = Lz77.decompress(buffer)
    xml = fromKBinXml(decoded)
    result = toObject(xml)
    
    if 'eacnet' in result:
        info = result['eacnet']['info']
        ctx.token = info['token']
        request = result['eacnet']['request']
        
        if not request:
            return await next()
        
        ctx.service = {
            'name': info['game_id'],
            'module': request['module'],
            'method': request['method']
        }
        
        ctx.body = request.get('data', {})
        
        if 'service' in request:
            ctx.acRelayInfo = {
                'module': request['module'],
                'method': request['method'],
                'request': xml['eacnet']['request']['data']
            }
        else:
            ctx.acRelayInfo = None
        
        return await next()
    
    game = list(result.keys())[0]
    
    if 'params' in result[game]:
        ctx.body = result['p2d']['params']
    else:
        ctx.body = {}
    
    ctx.service = {
        'name': game,
        'module': 'p2d',
        'method': result[game]['method']
    }
    
    ctx.token = getattr(body, 'p2d_token', None)
    
    return await next()
