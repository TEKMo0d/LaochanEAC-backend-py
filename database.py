from typing import Optional, Dict, Any
import asyncio
from pymongo import MongoClient
from utils.context import Logger
from utils.config import *
from .types.p2d.index import PlayerPlayData
from utils.kbinxml import fromKBinXml
from .types.p2d.pdata import Pdata

class DatabaseMeta:
    def __init__(self, version: int = 0):
        self.version = version

async def init_mongo_db():
    logger = Logger('database')

    logger.info('connecting to mongodb...')
    client = MongoClient(config.mongo_url)
    db = client[config.db_name]
    meta_col = db['__metadata']
    meta = meta_col.find_one({})
    if meta is None:
        meta = {"version": 0}

    if meta["version"] < 1:
        logger.info('upgrading database to ver 1')
        play_data_col = db['player_play_data']

        cursor = play_data_col.find({})
        tasks = []
        for player in cursor:
            pdata_obj = fromKBinXml(player["pdata"]["buffer"])
            pdata = pdata_obj["pdata"]

            tasks.append(play_data_col.update_one(
                {"_id": player["_id"]}, 
                {"$set": {
                    "djname": pdata["player"]["djname"],
                    "infinitas_id": pdata["player"]["infinitas_id"]
                }}
            ))

        await asyncio.gather(*tasks)

        logger.info(f'upgraded database to ver 1, effected {len(tasks)}')
        meta["version"] = 1

    if meta["version"] < 2:
        collections = await db.list_collection_names()
        
        async def try_rename_collection(src: str, dest: str):
            if src not in collections:
                return
                
            db[src].rename(dest)

        await asyncio.gather(
            try_rename_collection('player_play_data', 'p2d_play_data'),
            try_rename_collection('player_music_data', 'p2d_music_data'),
            try_rename_collection('player_play_log', 'p2d_play_log'),
            try_rename_collection('player_course_log', 'p2d_course_log'),
            try_rename_collection('player_customize_setting', 'p2d_customize_setting'),
            try_rename_collection('player_rival_data', 'p2d_rival_data'),
        )

        logger.info('upgraded database to ver 2, renamed prefix player to p2d.')
        meta["version"] = 2

    meta_col.update_one({}, {"$set": meta}, upsert=True)
    return db