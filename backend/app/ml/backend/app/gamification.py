from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/gamification", tags=["Gamification"])

# Mock leaderboard data
LEADERBOARD_DATA = [
    {"rank": 1, "username": "Alex Thompson", "points": 4850, "level": 15, "badges": 24, "avatar": "??"},
    {"rank": 2, "username": "Jordan Lee", "points": 4620, "level": 14, "badges": 22, "avatar": "??"},
    {"rank": 3, "username": "Casey Morgan", "points": 4390, "level": 13, "badges": 21, "avatar": "??"},
    {"rank": 4, "username": "Riley Cooper", "points": 4120, "level": 13, "badges": 19, "avatar": "4??"},
    {"rank": 5, "username": "Taylor Swift", "points": 3980, "level": 12, "badges": 18, "avatar": "5??"},
    {"rank": 6, "username": "Jamie Fox", "points": 3750, "level": 11, "badges": 17, "avatar": "6??"},
    {"rank": 7, "username": "Quinn Williams", "points": 3520, "level": 11, "badges": 16, "avatar": "7??"},
    {"rank": 8, "username": "Avery Johnson", "points": 3280, "level": 10, "badges": 15, "avatar": "8??"},
    {"rank": 9, "username": "Parker Lewis", "points": 3050, "level": 9, "badges": 14, "avatar": "9??"},
    {"rank": 10, "username": "Morgan Freeman", "points": 2890, "level": 9, "badges": 13, "avatar": "??"}
]

@router.get("/leaderboard")
async def get_leaderboard(limit: int = Query(20, ge=1, le=100)):
    """Get global leaderboard"""
    return {"leaderboard": LEADERBOARD_DATA[:limit], "total": len(LEADERBOARD_DATA)}

@router.get("/user/{user_id}/stats")
async def get_user_stats(user_id: int):
    """Get user statistics"""
    # Mock user stats
    return {
        "user_id": user_id,
        "username": "Current User",
        "level": 7,
        "total_points": 2450,
        "current_streak": 15,
        "badges_earned": 8,
        "rank": 42,
        "next_level_points": 2750,
        "points_to_next": 300,
        "recent_achievements": [
            {"name": "First Phishing Test", "date": "2024-01-15", "icon": "??"},
            {"name": "7-Day Streak", "date": "2024-02-01", "icon": "??"},
            {"name": "Perfect Score", "date": "2024-02-10", "icon": "??"}
        ]
    }

@router.get("/badges")
async def get_badges():
    """Get all available badges"""
    return {
        "badges": [
            {"name": "Phishing Expert", "description": "Complete 10 phishing tests", "icon": "??", "points": 100},
            {"name": "Security Champion", "description": "Perfect score on 5 tests", "icon": "??", "points": 200},
            {"name": "Streak Master", "description": "30-day streak", "icon": "??", "points": 300},
            {"name": "Early Bird", "description": "Complete tests before 9 AM", "icon": "??", "points": 150},
            {"name": "Night Owl", "description": "Complete tests after 10 PM", "icon": "??", "points": 150}
        ]
    }

@router.get("/challenges/active")
async def get_active_challenges():
    """Get active challenges"""
    return {
        "challenges": [
            {
                "id": 1,
                "name": "March Phishing Marathon",
                "description": "Complete 20 phishing tests this month",
                "points_reward": 500,
                "badge_reward": "Marathon Medal",
                "end_date": "2024-03-31",
                "participants": 234
            },
            {
                "id": 2,
                "name": "Streak Defender",
                "description": "Maintain a 14-day streak",
                "points_reward": 300,
                "badge_reward": None,
                "end_date": "2024-03-15",
                "participants": 178
            }
        ]
    }
