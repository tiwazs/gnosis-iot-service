from fastapi import APIRouter, Depends
from services.dependency import get_commands_service
from services.commandsService import CommandsService

router = APIRouter(prefix="/commands", tags=["Commands"])

@router.post("/")
async def send_command(command_id: int, data: dict = None, commands_service: CommandsService = Depends(get_commands_service)):
    return await commands_service.send_command(command_id, data)