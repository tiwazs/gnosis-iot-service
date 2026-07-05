from datetime import datetime
from typing import Annotated, List, Optional
from sqlalchemy import Column, Boolean, String, text, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
import uuid

IOT_SCHEMA = "iot"

class Base(DeclarativeBase):
    metadata = MetaData(schema=IOT_SCHEMA)

uuid_pk = Annotated[
    str, 
    mapped_column(String(36), primary_key=True, default = lambda: str( uuid.uuid4() ))
]

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")        
    ) 
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())"),
        onupdate=text("TIMEZONE('utc', NOW())")
    )

class Device(Base, TimestampMixin):
    __tablename__ = "devices"

    id: Mapped[uuid_pk]
    workspace_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    status: Mapped[bool] = mapped_column(default=False)
    coordinates: Mapped[List["Coordinate"]] = relationship(
        back_populates="device",
        cascade="all, delete-orphan"
    )

class Coordinate(Base, TimestampMixin):
    __tablename__ = "coordinates"

    id: Mapped[uuid_pk]
    device_id: Mapped[str] = mapped_column(String(36), ForeignKey("devices.id", ondelete="CASCADE") )
    device: Mapped["Device"] = relationship(back_populates="coordinates") 
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()

class Operation(Base, TimestampMixin):
    __tablename__ = "operations"

    id: Mapped[uuid_pk]
    workspace_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    actions: Mapped[List["Action"]] = relationship(back_populates="operation", cascade="all, delete-orphan")

class Action(Base, TimestampMixin):
    __tablename__ = "actions"

    id: Mapped[uuid_pk]
    operation_id: Mapped[str] = mapped_column(String(36), ForeignKey("operations.id", ondelete="CASCADE") )
    operation: Mapped["Operation"] = relationship(back_populates="actions")
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))





