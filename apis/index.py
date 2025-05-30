from fastapi import APIRouter, Depends, Request
from typing import Dict, Any, Optional
import logging

from .p2d.index import router as p2d_router
from ..utils.context import ILaochanContext, create_laochan_context

router = APIRouter(prefix='/api', tags=['api'])

router.include_router(p2d_router)

def get_routes():
    return router

async def get_context(request: Request) -> ILaochanContext:
    logger = logging.getLogger('api')
    
    token = request.headers.get('Authorization') or request.query_params.get('token')
    
    path_parts = request.url.path.strip('/').split('/')
    service_name = path_parts[1] if len(path_parts) > 1 else 'unknown'
    module = path_parts[2] if len(path_parts) > 2 else 'unknown'
    method = request.method.lower()
    
    body = None
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            body = await request.json()
        except:
            body = None
    
    context = create_laochan_context(
        service_name=service_name,
        module=module,
        method=method,
        logger=logger,
        token=token,
        body=body
    )
    
    return context

Context = ILaochanContext

api_router = router
