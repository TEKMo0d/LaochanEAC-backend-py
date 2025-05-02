from typing import List, Dict, Any
from bson import Binary, ObjectId
from dataclasses import dataclass, field

@dataclass
class RivalPatch:
    enabled: bool
    
@dataclass
class RivalPostOrDelete:
    infinitas_id: str
    type: int