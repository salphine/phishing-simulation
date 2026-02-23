from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.gamification import UserPoints, UserBadge, UserStreak, UserLevel
from services.gamification_service import gamification_service
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gamification", tags=["Gamification"])

@router.get("/leaderboard")
async def get_leaderboard(
    period: str = Query("all", description="Time period: daily, weekly, monthly, all"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get leaderboard with filtering by time period"""
    try:
        # Calculate date range based on period
        end_date = datetime.utcnow()
        if period == "daily":
            start_date = end_date - timedelta(days=1)
        elif period == "weekly":
            start_date = end_date - timedelta(weeks=1)
        elif period == "monthly":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = None  # All time
        
        # Get leaderboard from service
        leaderboard = await gamification_service.get_leaderboard(
            db=db, 
            limit=limit,
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "period": period,
            "count": len(leaderboard),
            "leaderboard": leaderboard
        }
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/badges")
async def get_available_badges(
    category: Optional[str] = Query(None, description="Badge category"),
    current_user: User = Depends(get_current_user)
):
    """Get all available badges with filtering by category"""
    try:
        badges = await gamification_service.get_available_badges(category=category)
        return {
            "total": len(badges),
            "badges": badges
        }
    except Exception as e:
        logger.error(f"Error getting badges: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/stats")
async def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive user gamification stats"""
    try:
        # Check if user has permission (admin or self)
        if current_user.id != user_id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to view this user's stats")
        
        stats = await gamification_service.get_comprehensive_user_stats(user_id, db)
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user/{user_id}/points/award")
async def award_points(
    user_id: int,
    points: int = Query(..., ge=1, le=1000),
    reason: str = Query(..., min_length=3, max_length=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Award points to a user (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        result = await gamification_service.award_points(
            user_id=user_id,
            points=points,
            reason=reason,
            awarded_by=current_user.id,
            db=db
        )
        return result
    except Exception as e:
        logger.error(f"Error awarding points: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/achievements/{user_id}")
async def get_user_achievements(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's achievements with progress"""
    try:
        achievements = await gamification_service.get_user_achievements(user_id, db)
        return achievements
    except Exception as e:
        logger.error(f"Error getting achievements: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/streaks/{user_id}")
async def get_user_streaks(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's current and historical streaks"""
    try:
        streaks = await gamification_service.get_user_streaks(user_id, db)
        return streaks
    except Exception as e:
        logger.error(f"Error getting streaks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/levels")
async def get_levels_config():
    """Get level configuration and requirements"""
    try:
        levels = await gamification_service.get_levels_config()
        return levels
    except Exception as e:
        logger.error(f"Error getting levels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/challenges/create")
async def create_challenge(
    name: str,
    description: str,
    points_reward: int,
    badge_reward: Optional[str] = None,
    start_date: datetime,
    end_date: datetime,
    requirements: Dict,
    current_user: User = Depends(get_current_user)
):
    """Create a new challenge (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        challenge = await gamification_service.create_challenge(
            name=name,
            description=description,
            points_reward=points_reward,
            badge_reward=badge_reward,
            start_date=start_date,
            end_date=end_date,
            requirements=requirements,
            created_by=current_user.id
        )
        return challenge
    except Exception as e:
        logger.error(f"Error creating challenge: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/challenges/active")
async def get_active_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get currently active challenges"""
    try:
        challenges = await gamification_service.get_active_challenges(db)
        return challenges
    except Exception as e:
        logger.error(f"Error getting challenges: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/challenges/{challenge_id}/join")
async def join_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Join a challenge"""
    try:
        result = await gamification_service.join_challenge(
            challenge_id=challenge_id,
            user_id=current_user.id,
            db=db
        )
        return result
    except Exception as e:
        logger.error(f"Error joining challenge: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/dashboard")
async def get_gamification_analytics(
    period: str = Query("month", description="week, month, quarter, year"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get gamification analytics dashboard (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        analytics = await gamification_service.get_analytics_dashboard(period, db)
        return analytics
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
