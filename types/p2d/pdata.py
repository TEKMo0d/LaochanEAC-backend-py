from typing import Dict, List, Any, TypedDict
from bson import Binary, ObjectId
from dataclasses import dataclass, field

class HistoryItem(TypedDict):
    time: int
    val: int

class History(TypedDict, total=False):
    __extra__: Dict[str, HistoryItem]

@dataclass
class Bit:
    boost_expire_date: int
    consume_bit: int
    total_bit: int

@dataclass
class Kind:
    id: int

@dataclass
class SPClass:
    kind: List[Kind] = field(default_factory=list)

@dataclass
class Dan:
    dp: SPClass = field(default_factory=SPClass)
    sp: SPClass = field(default_factory=SPClass)

@dataclass
class Effector:
    effect_type: int
    filter: int
    hi_eq: int
    hi_mid_eq: int
    low_eq: int
    low_mid_eq: int
    play_volume: int
    vefx: int

@dataclass
class Frame:
    expire_date: int

@dataclass
class FrameList:
    frame0: Frame
    frame1: Frame
    frame2: Frame

@dataclass
class Mission:
    frame_list: FrameList
    mission_list: History

@dataclass
class KeyConfig:
    sw_0: int
    sw_1: int
    sw_2: int
    sw_3: int
    sw_4: int
    sw_5: int
    sw_6: int
    sw_7: int
    sw_8: int
    sw_9: int
    sw_10: int
    sw_11: int
    sw_12: int
    sw_13: int
    sw_14: int
    sw_15: int
    sw_16: int
    sw_17: int
    sw_18: int
    sw_19: int
    sw_20: int
    sw_21: int
    sw_22: int
    sw_23: int
    sw_24: int
    sw_25: int
    sw_26: int
    sw_27: int
    sw_28: int
    sw_29: int
    sw_30: int
    sw_31: int
    sw_32: int
    sw_33: int
    sw_34: int
    sw_35: int

@dataclass
class Option:
    anykey_dp: int
    anykey_sp: int
    auto_scrach_disp_type_dp: int
    auto_scrach_disp_type_sp: int
    autoscratch_dp: int
    autoscratch_sp: int
    classic_hispeed_dp: int
    classic_hispeed_sp: int
    disp_judge_dp: bool
    disp_judge_sp: bool
    enable_auto_adjust_dp: bool
    enable_auto_adjust_sp: bool
    fivekeys_dp: int
    fivekeys_sp: int
    floating_hispeed_dp: int
    floating_hispeed_sp: int
    gauge_disp_type_dp: int
    gauge_disp_type_sp: int
    gauge_dp: int
    gauge_sp: int
    ghost_score_dp: int
    ghost_score_sp: int
    ghost_type_dp: int
    ghost_type_sp: int
    graph_no_dp: int
    graph_no_sp: int
    graph_position: int
    graph_score_type_dp: int
    graph_score_type_sp: int
    hidden_dp: int
    hidden_sp: int
    hispeed_dp: int
    hispeed_sp: int
    hispeed_type: int
    judge_adjust_dp: int
    judge_adjust_sp: int
    judge_place_dp: int
    judge_place_sp: int
    key_config: KeyConfig
    keyassist_dp: int
    keyassist_sp: int
    lane_brigntness_dp: int
    lane_brigntness_sp: int
    legacy_dp: int
    legacy_sp: int
    lift_dp: int
    lift_length_dp: int
    lift_length_sp: int
    lift_sp: int
    mirror_dp: int
    mirror_dp_2p: int
    mirror_sp: int
    movie_type_dp: int
    movie_type_sp: int
    music_sort_type_dp: int
    music_sort_type_sp: int
    notes_disp_time_dp: int
    notes_disp_time_sp: int
    option_style_dp: int
    option_style_sp: int
    pacemaker_dp: int
    pacemaker_sp: int
    random_dp: int
    random_dp_2p: int
    random_sp: int
    sd_length_dp: int
    sd_length_sp: int
    sd_type_dp: int
    sd_type_sp: int
    sub_graph_no_dp: int
    sub_graph_no_sp: int
    sudden_dp: int
    sudden_sp: int
    timing_disp_split_dp: int
    timing_disp_split_sp: int
    timing_type_dp: int
    timing_type_sp: int

@dataclass
class Player:
    achievement_dp: int
    achievement_sp: int
    djname: str
    grade_id_dp: int
    grade_id_sp: int
    infinitas_id: str
    play_num_dp: int
    play_num_sp: int
    pref_id: int

@dataclass
class Rival:
    challenge_crush_num_dp: int
    challenge_crush_num_sp: int

@dataclass
class CtrlHit:
    sw_01: int
    sw_02: int
    sw_03: int
    sw_04: int
    sw_05: int
    sw_06: int
    sw_07: int
    sw_08: int
    sw_09: int
    sw_10: int
    sw_11: int
    tt_mv: int

@dataclass
class Side:
    ctrl_count: int
    ctrl_hit: CtrlHit
    ctrl_type: int

@dataclass
class DPPlayTime:
    hist: History
    last_end: int
    last_start: int
    max: int
    total: int

@dataclass
class SPPlayTime:
    hist: History
    last_end: int
    last_start: int
    max: int
    total: int

@dataclass
class StatsDP:
    djpoint_hist: History
    grade_hist: History
    mrank_hist: History
    play_time: DPPlayTime

@dataclass
class SP:
    djpoint_hist: History
    grade_hist: History
    mrank_hist: History
    play_time: SPPlayTime

@dataclass
class Stats:
    dp: StatsDP
    left: Side
    right: Side
    sp: SP

@dataclass
class Pdata:
    bit: Bit
    dan: Dan
    effector: Effector
    mission: Mission
    option: Option
    player: Player
    rival: Rival
    stats: Stats
    version: str