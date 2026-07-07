import pytest
from unittest.mock import AsyncMock, MagicMock
from services.deviceService import DevicesService
from models.schema import Device

@pytest.mark.asyncio
async def test_device_service_selectall():
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

    service = DevicesService(mock_db)

    results = await service.get_devices()

    assert len(results) == 4
    assert results[0].name == "device1"

@pytest.mark.asyncio
async def test_device_service_getdevice():
    mock_db = AsyncMock()

    device = Device(id="abc", workspace_id="xyz", name="device", description="eee", status=False)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = device
    mock_db.execute.return_value = mock_result

    service = DevicesService(mock_db)

    result = await service.get_device(device_id="abc")

    assert result.name == "device"

@pytest.mark.asyncio
async def test_device_service_update():
    mock_db = AsyncMock()

    existing_device = Device(id="abc", workspace_id="xyz", name="old_name", description="eee", status=False)

    mock_result = MagicMock()
    mock_result.scalar_one_or_null.return_value = existing_device
    mock_db.execute.return_value = mock_result

    service = DevicesService(db = mock_db)

    fake_payload = {"name" : "new_name"}
    result = await service.update_device(device_id="abc" , device_in=fake_payload)

    assert result.name == "new_name"
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_device_service_delete():
    mock_db = AsyncMock()

    existing_device = Device(id="abc", workspace_id="xyz", name="old_name", description="eee", status=False)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_device
    mock_db.execute.return_value = mock_result
    
    service = DevicesService(mock_db)

    result = await service.delete_device(device_id="abc")

    mock_db.delete.assert_called_once_with(existing_device)
    mock_db.delete.assert_called_once()

    assert result == True
