import inspect
from typing import Any, Type


def Combine(*classes: Type[Any]) -> Type[Any]:
    class Modules:
        def __init__(self) -> None:
            for cls in classes:
                instance = cls()
                for attr_name, attr_value in instance.__dict__.items():
                    setattr(self, attr_name, attr_value)
    
    for cls in classes:
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if name != '__init__':
                setattr(Modules, name, method)
                
        for name, prop in inspect.getmembers(cls, predicate=lambda x: isinstance(x, property)):
            setattr(Modules, name, prop)
            
    return Modules

# 这里还存在一点问题我不知道怎么解决