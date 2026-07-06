from fastapi import APIRouter, Depends, HTTPException
from services.dependency import get_devices_service
from services.deviceService import DevicesService


router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/")
async def get_devices(devices_service: DevicesService = Depends(get_devices_service)):
    return await devices_service.get_devices()