from .deviceService import DevicesService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from clients.workspace_registration import WorkspaceRegistrationClient

def get_devices_service(db:AsyncSession = Depends(get_db)) -> DevicesService:
    return DevicesService(db)

def get_registration_client() -> WorkspaceRegistrationClient:
    return WorkspaceRegistrationClient()