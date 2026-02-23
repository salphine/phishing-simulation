from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/vishing", tags=["Vishing"])

# Mock data
MOCK_CALLS = [
    {"id": 1, "caller": "+1-555-0123", "duration": 245, "risk": "medium", "status": "active", "transcript": "This is your bank...", "timestamp": datetime.now().isoformat()},
    {"id": 2, "caller": "+1-555-7890", "duration": 180, "risk": "high", "status": "completed", "transcript": "Microsoft support...", "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat()},
    {"id": 3, "caller": "+1-555-4567", "duration": 90, "risk": "low", "status": "completed", "transcript": "Telemarketer call...", "timestamp": (datetime.now() - timedelta(hours=1)).isoformat()}
]

MOCK_CAMPAIGNS = [
    {"id": 1, "name": "Q1 Security Awareness", "active": True, "calls_made": 1245, "success_rate": 78, "start_date": "2024-01-15", "end_date": "2024-03-30"},
    {"id": 2, "name": "Tax Season Scams", "active": True, "calls_made": 892, "success_rate": 82, "start_date": "2024-02-01", "end_date": "2024-04-15"}
]

@router.get("/calls/active")
async def get_active_calls():
    """Get currently active vishing calls"""
    active_calls = [call for call in MOCK_CALLS if call["status"] == "active"]
    return {"active_calls": active_calls, "count": len(active_calls)}

@router.get("/calls/history")
async def get_call_history(limit: int = Query(50, ge=1, le=200)):
    """Get call history"""
    return {"calls": MOCK_CALLS[:limit], "total": len(MOCK_CALLS)}

@router.get("/analytics")
async def get_vishing_analytics(period: str = Query("day", regex="^(day|week|month)$")):
    """Get vishing analytics"""
    return {
        "period": period,
        "total_calls": 1245,
        "suspicious_calls": 234,
        "blocked_calls": 89,
        "success_rate": 81,
        "risk_distribution": {"low": 456, "medium": 567, "high": 222}
    }
