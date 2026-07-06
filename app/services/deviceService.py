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