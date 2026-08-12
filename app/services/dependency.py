from .deviceService import DevicesService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from clients.workspace_registration import WorkspaceRegistrationClient
from services.mqttClientService import MQTTClientService
from services.commandsService import CommandsService

def get_devices_service(db:AsyncSession = Depends(get_db)) -> DevicesService:
    return DevicesService(db)

def get_registration_client() -> WorkspaceRegistrationClient:
    return WorkspaceRegistrationClient()

def get_mqtt_client(request: Request) -> MQTTClientService:
    return request.app.state.mqtt

def get_commands_service(request: Request, mqtt_client: MQTTClientService = Depends(get_mqtt_client)) -> CommandsService:
    return CommandsService(mqtt_client)
