from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])

# Mock data
MOCK_CERTIFICATES = [
    {
        "id": "0x7a3f...8b2d",
        "name": "Phishing Expert Certification",
        "user": "Alex Thompson",
        "score": 98,
        "status": "verified",
        "issue_date": "2024-02-23"
    },
    {
        "id": "0x9b4e...2c1f",
        "name": "Security Champion",
        "user": "Jordan Lee",
        "score": 95,
        "status": "pending",
        "issue_date": "2024-02-22"
    },
    {
        "id": "0x3d8a...5e9b",
        "name": "Streak Master",
        "user": "Casey Morgan",
        "score": 100,
        "status": "verified",
        "issue_date": "2024-02-21"
    }
]

@router.get("/certificates")
async def get_certificates(limit: int = Query(10, ge=1, le=100)):
    """Get blockchain certificates"""
    return {"certificates": MOCK_CERTIFICATES[:limit], "total": len(MOCK_CERTIFICATES)}

@router.get("/stats")
async def get_blockchain_stats():
    """Get blockchain statistics"""
    return {
        "total_certificates": 1234,
        "verified_certificates": 1189,
        "pending_certificates": 45,
        "last_block": 89237
    }

@router.post("/verify")
async def verify_certificate(certificate_id: str):
    """Verify a certificate"""
    cert = next((c for c in MOCK_CERTIFICATES if c["id"] == certificate_id), None)
    if cert:
        return {"verified": cert["status"] == "verified", "certificate": cert}
    return {"verified": False, "message": "Certificate not found"}
