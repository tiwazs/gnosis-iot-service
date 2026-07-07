from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.schema import Device

class DevicesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_devices(self):
        statement = select(Device)
        result = await  self.db.execute(statement)

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
    
    async def update_device(self, device_id, device_in):

        statement = select(Device).where(Device.id == device_id)

        result = await self.db.execute(statement)

        device = result.scalar_one_or_none()

        if device:
            
            for key, value in device_in.items():
                if hasattr(device, key):
                    setattr(device, key, value)

            self.db.add(device)

            await self.db.commit()
            await self.db.refresh(device)
        
        return device