import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from models.schema import Device
from services.deviceService import DevicesService
from database.database import get_db
from main import app

@pytest.mark.asyncio
async def test_device_controller_getall(client):
    mock_db = AsyncMock()

    device1 = Device(id="a", workspace_id="x", name="device1", description="eee", status=False)
    device2 = Device(id="b", workspace_id="x", name="device2", description="eee", status=False)
    device3 = Device(id="c", workspace_id="y", name="device3", description="eee", status=False)
    device4 = Device(id="d", workspace_id="y", name="device4", description="eee", status=False)

    devices = [
        device1,
        device2,
        device3,
        device4
    ]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = devices
    mock_db.execute.return_value = mock_result

    app.dependency_overrides[get_db] = lambda: mock_db

    try:

        response = await client.get("/devices/")

        assert response.status_code == 200
        assert response.json()[0]["name"] == "device1"
        assert len(response.json()) == 4
    
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_device_controller_getdevice(client):
    mock_db = AsyncMock()

    device = Device(id="a", workspace_id="x", name="device1", description="eee", status=False)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = device
    mock_db.execute.return_value = mock_result

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = await client.get("devices/a")

        assert response.status_code == 200
        assert response.json()["name"] == "device1"
        assert response.json()["description"] == "eee"
    finally:

        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_device_controller_update(client):
    mock_db = AsyncMock()

    existing_device = Device(id="a", workspace_id="x", name="old_name", description="eee", status=False)
    
    update_payload = { "name": "new_name", "description": "dada" }

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_device
    mock_db.execute.return_value = mock_result

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = await client.patch(
            "devices/a",
            json=update_payload
        )

        assert response.json()["name"] == "new_name"
        assert response.json()["description"] == "dada"
        assert response.json()["status"] == False

    finally:
        app.dependency_overrides.clear()

