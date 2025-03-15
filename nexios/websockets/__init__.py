from .base import WebSocket, WebSocketDisconnect   # type:ignore
from .channels import Channel,ChannelBox
from .consumers import WebSocketEndpoint
import typing

Scope = typing.MutableMapping[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]

Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]


__all__ = [
    "WebSocket","Channel","ChannelBox","WebSocketEndpoint"
]