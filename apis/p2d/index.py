import logging
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pymongo.database import Database

from ...services.p2d.user import UserService
from ...types.p2d.index import PlayerCustomizeSetting, PlayerRivalData
from ...types.p2d.api import RivalPatch, RivalPostOrDelete
from ...database import init_mongo_db

logger = logging.getLogger('p2d-api')
router = APIRouter(prefix='/p2d', tags=['p2d'])

_db_instance = None

async def get_database() -> Database:
    global _db_instance
    if _db_instance is None:
        _db_instance = await init_mongo_db()
    return _db_instance

async def get_user_service(db: Database = Depends(get_database)) -> UserService:
    return UserService(db)

@router.get('/bot/player/{infinitas_id}')
async def get_player_by_infinitas_id(
    infinitas_id: str,
    user_service: UserService = Depends(get_user_service)
):
    if not infinitas_id:
        raise HTTPException(status_code=400, detail="infinitas_id is required")
    
    player = await user_service.find_player_by_infas_id(infinitas_id)
    
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return {
        "found": bool(player),
        "player": player
    }

@router.get('/pdata/{token}')
async def get_pdata(
    token: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get player data by token"""
    if not token:
        raise HTTPException(status_code=400, detail="token is required")
    
    logger.info('request pdata %s', token)
    pdata = await user_service.get_pdata_decoded(token)
    
    if not pdata:
        raise HTTPException(status_code=404, detail="Player data not found")
    
    return {"pdata": pdata}

@router.get('/customize/{token}')
async def get_customize(
    token: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get customize settings by token"""
    if not token:
        raise HTTPException(status_code=400, detail="token is required")
    
    logger.info('request customize %s', token)
    customize = await user_service.get_customize_setting(token)
    
    return {"customize": customize}

@router.get('/playlog/{token}')
async def get_playlog(
    token: str,
    skip: Optional[int] = Query(None),
    limit: Optional[int] = Query(None),
    user_service: UserService = Depends(get_user_service)
):
    """Get play logs by token with pagination"""
    result = user_service.get_play_logs(
        token, 
        skip if skip is not None else 0,
        limit if limit is not None else 10
    )
    
    return {"playLogs": result}

@router.get('/rival/{token}')
async def get_rival(
    token: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get rival data by token"""
    result = await user_service.get_player_rival_data(token)
    
    if not result.get('enabled', False):
        return {
            "enabled": False,
            "spRivals": [],
            "dpRivals": []
        }
    
    async def get_rival_player(tk: str) -> Dict[str, Any]:
        pdata = await user_service.get_pdata_decoded(tk)
        return pdata["player"] if pdata else None
    
    sp_rivals = []
    dp_rivals = []
    
    for sp_token in result.get('sp', []):
        rival_player = await get_rival_player(sp_token)
        if rival_player:
            sp_rivals.append(rival_player)
    
    for dp_token in result.get('dp', []):
        rival_player = await get_rival_player(dp_token)
        if rival_player:
            dp_rivals.append(rival_player)
    
    return {
        "enabled": True,
        "spRivals": sp_rivals,
        "dpRivals": dp_rivals
    }

@router.patch('/rival/{token}')
async def patch_rival(
    token: str,
    rival_patch: RivalPatch,
    user_service: UserService = Depends(get_user_service)
):
    """Update rival enabled status"""
    rival_data = PlayerRivalData(
        _id=token,
        enabled=rival_patch.enabled,
        sp=[],
        dp=[]  
    )
    
    await user_service.upsert_player_rival_data(rival_data)
    
    return {"success": True}

@router.post('/rival/{token}')
async def add_rival(
    token: str,
    rival_data: RivalPostOrDelete,
    user_service: UserService = Depends(get_user_service)
):
    if not rival_data.infinitas_id:
        raise HTTPException(status_code=400, detail="infinitas_id is undefined")
    
    existing = await user_service.get_player_rival_data(token)
    target_info = await user_service.find_player_by_infas_id(rival_data.infinitas_id)
    
    if not target_info:
        raise HTTPException(status_code=404, detail="rival target not found")
    
    target = target_info["player"]
    
    if target == token:
        raise HTTPException(status_code=400, detail="ni rival ni zi ji?")
    
    target_array = existing["dp"] if rival_data.type else existing["sp"]
    
    if target in target_array:
        raise HTTPException(status_code=400, detail="rival target already exists")
    
    target_array.append(target)
    
    await user_service.upsert_player_rival_data(existing)
    
    return {"success": True}

@router.delete('/rival/{token}')
async def delete_rival(
    token: str,
    rival_data: RivalPostOrDelete,
    user_service: UserService = Depends(get_user_service)
):
    existing = await user_service.get_player_rival_data(token)
    target_info = await user_service.find_player_by_infas_id(rival_data.infinitas_id)
    
    target = target_info["player"] if target_info else None
    
    if rival_data.type:  # DP
        existing["dp"] = [v for v in existing["dp"] if v != target]
    else:  # SP
        existing["sp"] = [v for v in existing["sp"] if v != target]
    
    await user_service.upsert_player_rival_data(existing)
    
    return {"success": True}

@router.put('/customize/{token}')
async def update_customize(
    token: str,
    customize: PlayerCustomizeSetting,
    user_service: UserService = Depends(get_user_service)
):
    if not token:
        raise HTTPException(status_code=400, detail="token is required")
    
    logger.info('set customize %s', token)
    
    if not customize:
        raise HTTPException(status_code=400, detail="customize data is required")
    
    customize["_id"] = token
    await user_service.upsert_customize_setting(customize)
    
    return {"success": True}
