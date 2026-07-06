from .deviceService import DevicesService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

def get_devices_service(db:AsyncSession = Depends(get_db)) -> DevicesService:
    return DevicesService(db)