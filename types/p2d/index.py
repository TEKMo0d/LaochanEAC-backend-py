from typing import List, Dict, Any
from bson import Binary, ObjectId
from dataclasses import dataclass, field


@dataclass
class PlayerPlayData:
    _id: str
    # konami binary xml
    pdata: Binary
    # sha256 to ^
    check_sum: str
    djname: str
    infinitas_id: str


@dataclass
class PlayerRivalData:
    _id: str
    enabled: bool
    sp: List[str]
    dp: List[str]

@dataclass
class PlayerMusicData:
    player: str
    music_id: int
    play_style: int
    score: List[int]
    clear_flag: List[int]
    miss_count: List[int]
    play_num: List[int]
    clear_num: List[int]
    best_score_clock: List[int]

@dataclass
class PlayerPlayLog:
    _id: ObjectId
    player: str
    clock: int
    music_id: int
    note_id: int
    score: int
    pgreat_count: int
    great_count: int
    miss_count: int
    clear_flag: int
    stage: int
    groove_gauge: int
    mode_id: int
    mode_sub_id: int
    fail_detail: int
    ghost_check_sum: str
    update_my_best_score: bool
    is_limit_score: bool
    rival_infinitas_id: str
    is_compe: bool
    compe_id: int
    compe_music_index: int
    valid_best_option: bool
    arrange_0: int
    arrange_1: int
    assist: int
    flip: int
    ghost: Binary
    modifier: int

@dataclass
class CourseStage:
    stage_num: int
    clear_flag: int
    dj_level: int
    clear_rate: int
    groove_gage: int

@dataclass
class CourseResult:
    clear_type: int
    max_combo: int
    clear_rate: int
    groove_gage: int


@dataclass
class PlayerCourseLog:
    _id: ObjectId
    player: str
    playstyle: int
    kind: int
    grade_id: int
    stage: CourseStage
    total: CourseResult


@dataclass
class PlayerCustomizeSetting:
    _id: str
    items_count: Dict[str, int] = field(default_factory=lambda: {
        "bit": 0,
        "ldisc": 0,
        "infinitas_ticket": 0,
        "infinitas_ticket_free": 0
    })
    customize: List[Dict[str, Any]] = field(default_factory=list)
    other_customize: List[Dict[str, Any]] = field(default_factory=list)