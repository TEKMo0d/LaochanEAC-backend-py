from typing import Dict, List, Union, Any, TypeVar, Generic, Callable, Optional
from datetime import datetime

VALUE_TYPES = [
    's8', 'u8', 's16', 'u16', 's32', 'u32', 's64', 'u64',
    'float', 'double', 'b', 'bool', 'bin', 'binary',
    'ip4', 'str', 'string', 'time'
]

T = TypeVar('T')
VT = TypeVar('VT')

class KValueG(Dict[str, Any]):
    def __init__(self, type_name: str, value: Any, attrs: Optional[Dict[str, Any]] = None):
        super().__init__()
        self["$__type"] = type_name
        self["__value"] = value
        
        if attrs:
            for key, val in attrs.items():
                self[f"${key}"] = val

class KS8(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('s8', value, attrs)

class KU8(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('u8', value, attrs)

class KS16(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('s16', value, attrs)

class KU16(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('u16', value, attrs)

class KS32(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('s32', value, attrs)

class KU32(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('u32', value, attrs)

class KS64(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('s64', value, attrs)

class KU64(KValueG): 
    def __init__(self, value: Union[int, List[int]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('u64', value, attrs)

class KFloat(KValueG): 
    def __init__(self, value: Union[float, List[float]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('float', value, attrs)

class KDouble(KValueG): 
    def __init__(self, value: Union[float, List[float]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('double', value, attrs)

class KBoolean(KValueG): 
    def __init__(self, value: Union[bool, List[bool]], type_name: str = 'bool', attrs: Optional[Dict[str, Any]] = None):
        super().__init__(type_name, value, attrs)

class KBinary(KValueG): 
    def __init__(self, value: Union[bytes, List[bytes]], type_name: str = 'bin', attrs: Optional[Dict[str, Any]] = None):
        super().__init__(type_name, value, attrs)

class KString(KValueG): 
    def __init__(self, value: Union[str, List[str]], type_name: str = 'str', attrs: Optional[Dict[str, Any]] = None):
        super().__init__(type_name, value, attrs)

class KIPv4(KValueG): 
    def __init__(self, value: Union[str, List[str]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('ip4', value, attrs)

class KTime(KValueG): 
    def __init__(self, value: Union[datetime, int, List[Union[datetime, int]]], attrs: Optional[Dict[str, Any]] = None):
        super().__init__('time', value, attrs)

KValue = Union[KS8, KU8, KS16, KU16, KS32, KU32, KS64, KU64, KFloat, KDouble, KBoolean, KBinary, KString, KIPv4, KTime]

#to-do
'''
export type Serializable = {
  [key: string]: KValue | Serializable | Serializable[]
} | AttributeProperty<{
  [key: string]: string | number;
}>;
'''
#i have no idea to use type AttributeProperty in it
Serializable = Union[
    Dict[str, Union[KValue, 'Serializable', List['Serializable']]],  
    Dict[str, Union[str, int]]
]

def vg(type_name: str):
    def creator(value: Any, attrs: Optional[Dict[str, Any]] = None) -> KValueG:
        result = KValueG(type_name, value, attrs)
        return result
    return creator

class V:
    def __init__(self):
        self.s8 = vg('s8')
        self.u8 = vg('u8')
        self.s16 = vg('s16')
        self.u16 = vg('u16')
        self.s32 = vg('s32')
        self.u32 = vg('u32')
        self.s64 = vg('s64')
        self.u64 = vg('u64')
        self.float = vg('float')
        self.double = vg('double')
        self.b = vg('b')
        self.bool = vg('bool')
        self.bin = vg('bin')
        self.binary = vg('binary')
        self.ip4 = vg('ip4')
        self.str = vg('str')
        self.string = vg('string')
        self.time = vg('time')

v = V()