from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.schema import Device
from clients.workspace_registration import WorkspaceRegistrationClient
from grpc.aio import AioRpcError

class DevicesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_devices(self):
        statement = select(Device)
        result = await  self.db.execute(statement)

        return result.scalars().all()

    async def get_devices_by_workspace(self, workspace_id):
        statement = select(Device).where(Device.workspace_id == workspace_id)

        result = await self.db.execute(statement)

        return result.scalars().all()
    
    async def get_device(self, device_id):
        statement = select(Device).where(Device.id == device_id)

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def create_device(self, device_in):
        new_device = Device(**device_in)

        self.db.add(new_device)

        await self.db.commit()
        await self.db.refresh(new_device)

        return new_device

    async def register_device(self, data: dict, registration_client: WorkspaceRegistrationClient) -> Device:
        try:
            redeemed = await registration_client.redeem_token(data["token"])
        except AioRpcError as e:
            raise e

        device_in = {
            "workspace_id": redeemed.workspace_id,
            "name": data["name"],
            "description": data.get("description", ""),
            "status": data.get("status", False),
        }
        return await self.create_device(device_in)
    
    async def update_device(self, device_id, device_in):

        statement = select(Device).where(Device.id == device_id)

        result = await self.db.execute(statement)

        device = result.scalar_one_or_none()

        if device:
            
            for key, value in device_in.items():
                if hasattr(device, key):
                    setattr(device, key, value)

            await self.db.add(device)

            await self.db.commit()
            await self.db.refresh(device)
        
        return device
    
    async def delete_device(self, device_id):
        statement = select(Device).where(Device.id == device_id)

        result = await self.db.execute(statement)

        device = result.scalar_one_or_none()

        if device:
            await self.db.delete(device)
            await self.db.commit()

            return True
    
        return False