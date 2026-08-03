from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RedeemTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class RedeemTokenResponse(_message.Message):
    __slots__ = ("workspace_id", "created_by")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    created_by: str
    def __init__(self, workspace_id: _Optional[str] = ..., created_by: _Optional[str] = ...) -> None: ...
