from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional, List

router = APIRouter(prefix="/integrations", tags=["Integrations"])

# Mock data
MOCK_WEBHOOKS = [
    {"id": 1, "name": "Slack", "url": "https://hooks.slack.com/...", "events": ["phishing.detected"], "status": "active"},
    {"id": 2, "name": "Teams", "url": "https://outlook.office.com/...", "events": ["user.login"], "status": "active"}
]

MOCK_SIEM_CONFIGS = [
    {"id": 1, "provider": "Splunk", "endpoint": "https://splunk:8089", "status": "active"},
    {"id": 2, "provider": "ELK", "endpoint": "https://elastic:9200", "status": "active"}
]

MOCK_HRIS_SYNCS = [
    {"id": 1, "provider": "Workday", "status": "completed", "records_synced": 234, "completed_at": datetime.now().isoformat()}
]

@router.get("/webhooks")
async def get_webhooks():
    """Get all webhooks"""
    return {"webhooks": MOCK_WEBHOOKS, "total": len(MOCK_WEBHOOKS)}

@router.get("/hris/status")
async def get_hris_status():
    """Get HRIS integration status"""
    return {
        "provider": "Workday",
        "status": "active",
        "last_sync": datetime.now().isoformat(),
        "total_employees": 1234
    }

@router.get("/hris/sync-history")
async def get_hris_sync_history(limit: int = Query(10, ge=1, le=50)):
    """Get HRIS sync history"""
    return {"syncs": MOCK_HRIS_SYNCS[:limit], "total": len(MOCK_HRIS_SYNCS)}

@router.get("/siem/configs")
async def get_siem_configs():
    """Get SIEM configurations"""
    return {"configs": MOCK_SIEM_CONFIGS, "total": len(MOCK_SIEM_CONFIGS)}
