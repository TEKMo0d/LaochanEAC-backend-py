from typing import Dict, Any, TypeVar, Optional, Protocol, Callable, Type
from typing_extensions import TypedDict
from dependency_injector import containers, providers

from utils.kxml_value import Serializable

class AcRelayInfo(TypedDict):
    module: str
    method: str
    request: Serializable

class Logger(Protocol):
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def warn(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: ...

T = TypeVar('T')

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
container = Container()

ResolveFunc = Callable[[Type[T]], T]

class ILaochanContext(TypedDict, total=False):
    token: Optional[str]
    
    service: Dict[str, str]
    
    acRelayInfo: Optional[AcRelayInfo]
    
    logger: Logger
    
    body: Any
    
    resolve: ResolveFunc

Context = Dict[str, Any]

def resolve_dependency(dependency_type: Type[T]) -> T:
    return container.resolve(dependency_type)

def create_laochan_context(
    service_name: str,
    module: str,
    method: str,
    logger: Logger,
    token: Optional[str] = None,
    ac_relay_info: Optional[AcRelayInfo] = None,
    body: Any = None
) -> ILaochanContext:

    context: ILaochanContext = {
        'service': {
            'name': service_name,
            'module': module,
            'method': method,
        },
        'logger': logger,
        'resolve': resolve_dependency
    }
    
    if token is not None:
        context['token'] = token
        
    if ac_relay_info is not None:
        context['acRelayInfo'] = ac_relay_info
        
    if body is not None:
        context['body'] = body
        
    return context

def configure_container(config_dict: Dict[str, Any]) -> None:
    container.config.from_dict(config_dict)