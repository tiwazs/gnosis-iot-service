from fastapi import APIRouter, Depends, HTTPException
from services.dependency import get_devices_service
from services.deviceService import DevicesService
from models.deviceDTO import DeviceCreateDTO, DeviceUpdateDTO
import json


router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/")
async def get_devices(devices_service: DevicesService = Depends(get_devices_service)):
    return await devices_service.get_devices()


@router.get("/{device_id}")
async def get_device(device_id: int, devices_service: DevicesService = Depends(get_devices_service)):
    device =  await devices_service.get_device(device_id)

    if not device:
        return HTTPException(status_code=404, detail="Device not found")

    return device

@router.post("/")
async def create_device(device_data: DeviceCreateDTO, devices_service: DevicesService = Depends(get_devices_service)):
    return await devices_service.create_device(device_data.model_dump(exclude_none=True))

@router.patch("/{device_id}")
async def update_device(device_id: str, device_data: DeviceUpdateDTO, devices_service: DevicesService = Depends(get_devices_service)):
    updated_device = await devices_service.update_device(device_id, device_data.model_dump(exclude_none=True))

    if not updated_device:
        return HTTPException(status_code = 404, detail = "Device not found")

    return updated_device