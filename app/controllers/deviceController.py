from fastapi import APIRouter, Depends, HTTPException
from services.dependency import get_devices_service, get_registration_client
from services.deviceService import DevicesService
from models.deviceDTO import DeviceCreateDTO, DeviceUpdateDTO
import json
from grpc.aio import AioRpcError

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/")
async def get_devices(devices_service: DevicesService = Depends(get_devices_service)):
    return await devices_service.get_devices()


@router.get("/{workspace_id}")
async def get_devices_by_workspace(workspace: str, devices_service: ServicesService = Depends(get_services_service)):
    return await devices_service.get_devices_by_workspace(workspace)

@router.get("/{device_id}")
async def get_device(device_id: str, devices_service: DevicesService = Depends(get_devices_service)):
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

@router.post("/register/{registration_token}")
async def register_device(
        registration_token: str, 
        devices_service: DevicesService = Depends(get_devices_service),
        registration_client = Depends(get_registration_client),
    ):
    try:
        return await devices_service.register_device(
            {
                "token": registration_token,
                "name": "Device 1",
                "description": "Device 1 description",
                "status": False,
            },
            registration_client,
        )
    except AioRpcError as e:
        raise HTTPException(status_code=400, detail="invalid or expired token")