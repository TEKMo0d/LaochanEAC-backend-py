from bson.binary import Binary
from pymongo.database import Database
from typing import Dict, Any, Optional, cast
from pymongo.collection import Collection
from utils.kbinxml import fromKBinXml
from ...types.p2d.index import (
    PlayerPlayData,
    PlayerMusicData,
    PlayerPlayLog,
    PlayerCourseLog,
    PlayerCustomizeSetting,
    PlayerRivalData
)

class UserService:
    def __init__(self, db: Database):
        self.db = db

    @property
    def play_data_col(self) -> Collection[PlayerPlayData]:
        return cast(Collection[PlayerPlayData], self.db.get_collection('p2d_play_data'))

    @property
    def music_data_col(self) -> Collection[PlayerMusicData]:
        return cast(Collection[PlayerMusicData], self.db.get_collection("p2d_music_data"))

    @property
    def play_log_col(self) -> Collection[PlayerPlayLog]:
        return cast(Collection[PlayerPlayLog], self.db.get_collection('p2d_play_log'))

    @property
    def course_log_col(self) -> Collection[PlayerCourseLog]:
        return cast(Collection[PlayerCourseLog], self.db.get_collection('p2d_course_log'))

    @property
    def customize_setting_col(self) -> Collection[PlayerCustomizeSetting]:
        return cast(Collection[PlayerCustomizeSetting], self.db.get_collection('p2d_customize_setting'))

    @property
    def rival_data_col(self) -> Collection[PlayerRivalData]:
        return cast(Collection[PlayerRivalData], self.db.get_collection('p2d_rival_data'))

    def add_course_log(self, course_log: PlayerCourseLog):
        return self.course_log_col.insert_one(course_log)

    def add_play_log(self, play_log: PlayerPlayLog):
        return self.play_log_col.insert_one(play_log)

    def get_play_logs(self, player: str, skip=0, limit=10):
        return list(self.play_log_col.find(
            {"player": player},
            sort=[("player", 1), ("clock", -1)],
            skip=skip,
            limit=limit
        ))

    def get_course_logs(self, player: str, skip=0, limit=10):
        return list(self.course_log_col.find(
            {"player": player},
            sort=[("player", 1), ("_id", -1)],
            skip=skip,
            limit=limit
        ))

    def upsert_customize_setting(self, customize_setting: PlayerCustomizeSetting):
        return self.customize_setting_col.update_one(
            {"_id": customize_setting["_id"]},
            {"$set": customize_setting},
            upsert=True
        )

    async def get_customize_setting(self, player: str) -> PlayerCustomizeSetting:
        result = await self.customize_setting_col.find_one({"_id": player})
        if result:
            if "items_count" not in result or result["items_count"] is None:
                result["items_count"] = {
                    "bit": 15000,
                    "ldisc": 5,
                    "infinitas_ticket": 50,
                    "infinitas_ticket_free": 9,
                }

            if not any(item["item_category"] == 12 for item in result["customize"]):
                result["customize"].append({"item_category": 12, "item_id": "I2100000"})

            return result

        return {
            "_id": player,
            "items_count": {
                "bit": 15000,
                "ldisc": 5,
                "infinitas_ticket": 50,
                "infinitas_ticket_free": 9,
            },
            "customize": [
                {"item_category": 2, "item_id": "I1100000"},
                {"item_category": 3, "item_id": "I1200000"},
                {"item_category": 4, "item_id": "I1300000"},
                {"item_category": 5, "item_id": "I1400000"},
                {"item_category": 6, "item_id": "I1500000"},
                {"item_category": 7, "item_id": "I1600000"},
                {"item_category": 8, "item_id": "I1700000"},
                {"item_category": 11, "item_id": "I1300000"},
                {"item_category": 10, "item_id": "I1900000"},
                {"item_category": 12, "item_id": "I2100000"},
            ],
            "other_customize": [
                {"item_category": 1, "item_id": "C1000000"},
                {"item_category": 2, "item_id": "C1100000"},
                {"item_category": 3, "item_id": "C1200000"},
                {"item_category": 4, "item_id": "C1300000"},
                {"item_category": 5, "item_id": "C1400002"},
            ]
        }

    async def get_pdata_checksum(self, player: str) -> Optional[str]:
        result = await self.play_data_col.find_one(
            {"_id": player},
            projection={"check_sum": 1}
        )

        if result:
            return result.get("check_sum")
        
        return None

    async def find_player_by_infas_id(self, infinitas_id: str) -> Optional[Dict[str, str]]:
        result = await self.play_data_col.find_one(
            {"infinitas_id": infinitas_id},
            projection={"_id": 1, "djname": 1}
        )

        if result:
            return {"player": result["_id"], "djname": result["djname"]}
        
        return None

    async def get_pdata_binary(self, player: str) -> Optional[Dict[str, Any]]:
        result = await self.play_data_col.find_one({"_id": player})

        if not result:
            return None

        return {
            "pdata": bytes(result["pdata"]),
            "check_sum": result["check_sum"],
        }

    async def get_pdata_decoded(self, player: str):
        binary = await self.get_pdata_binary(player)
        if not binary:
            return None

        return fromKBinXml(binary["pdata"])["pdata"]

    def upsert_pdata_binary(self, player: str, pdata: bytes, check_sum: str):
        unpacked = fromKBinXml(pdata)
        pdata_obj = unpacked["pdata"]
        djname = pdata_obj["player"]["djname"]
        infinitas_id = pdata_obj["player"]["infinitas_id"]

        return self.play_data_col.update_one(
            {"_id": player},
            {"$set": {
                "djname": djname,
                "infinitas_id": infinitas_id,
                "pdata": Binary(pdata),
                "check_sum": check_sum,
            }},
            upsert=True
        )

    def get_music_datas(self, player: str, play_style: int) -> PlayerMusicData:
        return list(self.music_data_col.find({
            "player": player,
            "play_style": play_style,
        }))

    def get_play_log(self, player: str, clock: int) -> PlayerPlayLog:
        return self.play_log_col.find_one({
            "player": player,
            "clock": clock,
        })

    async def get_music_data(self, player: str, music_id: int, play_style: int) -> PlayerMusicData:
        result = await self.music_data_col.find_one({
            "player": player,
            "music_id": music_id,
            "play_style": play_style,
        })

        if result:
            if "best_score_clock" not in result or result["best_score_clock"] is None:
                result["best_score_clock"] = [-1, -1, -1, -1, -1]
            return result

        return {
            "player": player,
            "music_id": music_id,
            "play_style": play_style,
            "score": [0, 0, 0, 0, 0],
            "clear_flag": [0, 0, 0, 0, 0],
            "miss_count": [-1, -1, -1, -1, -1],
            "play_num": [0, 0, 0, 0, 0],
            "clear_num": [0, 0, 0, 0, 0],
            "best_score_clock": [-1, -1, -1, -1, -1],
        }

    def upsert_music_data(self, music_data: PlayerMusicData):
        return self.music_data_col.update_one(
            {
                "player": music_data["player"],
                "music_id": music_data["music_id"],
                "play_style": music_data["play_style"]
            },
            {"$set": music_data},
            upsert=True
        )

    async def get_player_rival_data(self, player: str) -> PlayerRivalData:
        result = await self.rival_data_col.find_one({"_id": player})

        if result:
            if "dp" not in result or result["dp"] is None:
                result["dp"] = []
            if "sp" not in result or result["sp"] is None:
                result["sp"] = []
            
            return result

        return {
            "_id": player,
            "enabled": False,
            "sp": [],
            "dp": [],
        }

    def upsert_player_rival_data(self, rival_data: PlayerRivalData):
        return self.rival_data_col.update_one(
            {"_id": rival_data["_id"]},
            {"$set": rival_data},
            upsert=True
        )
