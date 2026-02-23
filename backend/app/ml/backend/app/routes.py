from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.gamification import (
    UserPoints, UserBadge, UserStreak,
    ChallengeParticipation, RewardRedemption,
    PointTransaction
)
from services.gamification_service import gamification_service
from datetime import datetime
import secrets

router = APIRouter()

@router.get("/profile/{user_id}")
async def get_gamification_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's complete gamification profile"""
    
    # Get points
    points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
    if not points:
        points = UserPoints(user_id=user_id)
        db.add(points)
        db.commit()
        db.refresh(points)
    
    # Get badges
    badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
    
    # Get streak
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    
    return {
        "user_id": user_id,
        "points": points.total_points if points else 0,
        "level": points.level if points else 1,
        "badges": [{"name": b.badge_name, "type": b.badge_type} for b in badges],
        "current_streak": streak.current_streak if streak else 0,
        "longest_streak": streak.longest_streak if streak else 0
    }
