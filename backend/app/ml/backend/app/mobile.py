from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/mobile", tags=["Mobile"])

# Mock data
MOCK_DEVICES = [
    {"id": 1, "device_name": "iPhone 14 Pro", "device_type": "iOS", "status": "active", "last_active": datetime.now().isoformat()},
    {"id": 2, "device_name": "iPad Air", "device_type": "iOS", "status": "active", "last_active": datetime.now().isoformat()},
    {"id": 3, "device_name": "Pixel 7", "device_type": "Android", "status": "inactive", "last_active": (datetime.now() - timedelta(hours=2)).isoformat()}
]

@router.get("/devices")
async def get_devices():
    """Get all mobile devices"""
    return {"devices": MOCK_DEVICES, "total": len(MOCK_DEVICES)}

@router.get("/analytics")
async def get_mobile_analytics():
    """Get mobile analytics"""
    return {
        "total_devices": 3,
        "active_devices": 2,
        "open_rate": 81
    }
