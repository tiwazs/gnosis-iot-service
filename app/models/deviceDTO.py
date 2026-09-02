from pydantic import BaseModel
from typing import Optional

class DeviceCreateDTO(BaseModel):
    workspace_id: str
    name: str
    description: Optional[str] = ""
    status: bool = False

class DeviceUpdateDTO(BaseModel):
    workspace_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
