from typing import Dict, List, Any
from datetime import datetime, timedelta
import numpy as np
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class GamificationService:
    """
    Comprehensive gamification engine with badges, levels, and rewards
    """
    
    def __init__(self):
        self.badges = self._initialize_badges()
        self.levels = self._initialize_levels()
        self.challenges = self._initialize_challenges()
        self.rewards = self._initialize_rewards()
    
    def _initialize_badges(self) -> Dict[str, Dict]:
        """Initialize all achievement badges"""
        return {
            # Security Awareness Badges
            'phishing_spotter': {
                'name': '🕵️ Phishing Spotter',
                'description': 'Correctly identified 10 phishing emails',
                'category': 'awareness',
                'tiers': ['bronze', 'silver', 'gold', 'platinum'],
                'requirements': {'correct_identifications': [10, 50, 200, 500]},
                'points': [100, 500, 2000, 5000],
                'icon': '🛡️'
            },
            'vigilant_guardian': {
                'name': '🛡️ Vigilant Guardian',
                'description': 'Reported suspicious emails to security team',
                'category': 'proactive',
                'tiers': ['bronze', 'silver', 'gold', 'platinum'],
                'requirements': {'reports': [5, 20, 50, 100]},
                'points': [150, 600, 2500, 6000],
                'icon': '⚔️'
            },
            
            # Training Excellence Badges
            'training_master': {
                'name': '🎓 Training Master',
                'description': 'Completed all training modules with perfect scores',
                'category': 'training',
                'tiers': ['bronze', 'silver', 'gold', 'platinum'],
                'requirements': {'modules_completed': [5, 15, 30, 50], 'avg_score': [80, 90, 95, 100]},
                'points': [200, 800, 3000, 8000],
                'icon': '📚'
            },
            'speed_learner': {
                'name': '⚡ Speed Learner',
                'description': 'Completed training modules faster than average',
                'category': 'training',
                'tiers': ['bronze', 'silver', 'gold'],
                'requirements': {'speed_percentile': [50, 75, 90]},
                'points': [100, 400, 1500],
                'icon': '🏃'
            },
            
            # Behavior Improvement Badges
            'comeback_king': {
                'name': '👑 Comeback King',
                'description': 'Reduced risk score by 50% after training',
                'category': 'improvement',
                'tiers': ['bronze', 'silver', 'gold'],
                'requirements': {'improvement_percent': [30, 50, 70]},
                'points': [300, 1000, 4000],
                'icon': '📈'
            },
            'zero_risk_hero': {
                'name': '🦸 Zero Risk Hero',
                'description': 'Maintained zero security incidents for 6 months',
                'category': 'achievement',
                'tiers': ['gold', 'platinum', 'diamond'],
                'requirements': {'days_safe': [180, 365, 730]},
                'points': [5000, 15000, 50000],
                'icon': '🏆'
            },
            
            # Social Badges
            'team_player': {
                'name': '🤝 Team Player',
                'description': 'Helped colleagues improve their security awareness',
                'category': 'social',
                'tiers': ['bronze', 'silver', 'gold'],
                'requirements': {'team_assists': [5, 20, 50]},
                'points': [100, 400, 1500],
                'icon': '👥'
            },
            'security_influencer': {
                'name': '📢 Security Influencer',
                'description': 'Shared security tips that helped others',
                'category': 'social',
                'tiers': ['bronze', 'silver', 'gold', 'platinum'],
                'requirements': {'shares_helpful': [10, 50, 200, 500]},
                'points': [150, 600, 2500, 8000],
                'icon': '🎙️'
            },
            
            # Department Competition Badges
            'department_champion': {
                'name': '🏆 Department Champion',
                'description': 'Highest security score in department',
                'category': 'competition',
                'tiers': ['monthly', 'quarterly', 'yearly'],
                'requirements': {'rank': [1, 1, 1], 'period': ['month', 'quarter', 'year']},
                'points': [1000, 5000, 20000],
                'icon': '👑'
            },
            
            # Special Achievement Badges
            'early_adopter': {
                'name': '🌅 Early Adopter',
                'description': 'Joined the security awareness program in first month',
                'category': 'special',
                'tiers': ['unique'],
                'requirements': {'join_date': 'special'},
                'points': 1000,
                'icon': '🌟'
            },
            'phishing_terminator': {
                'name': '🤖 Phishing Terminator',
                'description': 'Identified and reported a zero-day phishing attempt',
                'category': 'special',
                'tiers': ['unique'],
                'requirements': {'zero_day_report': True},
                'points': 10000,
                'icon': '💀'
            }
        }
    
    def _initialize_levels(self) -> List[Dict]:
        """Initialize user levels with requirements"""
        return [
            {'level': 1, 'name': 'Security Novice', 'min_points': 0, 'benefits': ['Basic access']},
            {'level': 2, 'name': 'Security Apprentice', 'min_points': 500, 'benefits': ['Badge display']},
            {'level': 3, 'name': 'Security Practitioner', 'min_points': 2000, 'benefits': ['Advanced training access']},
            {'level': 4, 'name': 'Security Specialist', 'min_points': 5000, 'benefits': ['Mentor others']},
            {'level': 5, 'name': 'Security Expert', 'min_points': 10000, 'benefits': ['Beta features']},
            {'level': 6, 'name': 'Security Master', 'min_points': 25000, 'benefits': ['Reward redemption']},
            {'level': 7, 'name': 'Security Guru', 'min_points': 50000, 'benefits': ['Priority support']},
            {'level': 8, 'name': 'Security Legend', 'min_points': 100000, 'benefits': ['Named in hall of fame']},
            {'level': 9, 'name': 'Security Myth', 'min_points': 250000, 'benefits': ['Custom badge design']},
            {'level': 10, 'name': 'Security God', 'min_points': 500000, 'benefits': ['Lifetime achievement award']}
        ]
    
    def _initialize_challenges(self) -> List[Dict]:
        """Initialize weekly/monthly challenges"""
        return [
            {
                'id': 'weekly_spotter',
                'name': 'Weekly Spotter Challenge',
                'description': 'Correctly identify 5 phishing emails this week',
                'type': 'weekly',
                'requirements': {'identifications': 5},
                'reward_points': 500,
                'reward_badge': 'phishing_spotter_bronze',
                'icon': '🎯'
            },
            {
                'id': 'monthly_master',
                'name': 'Monthly Training Master',
                'description': 'Complete all assigned training with >90% score',
                'type': 'monthly',
                'requirements': {'completion_rate': 100, 'min_score': 90},
                'reward_points': 2000,
                'reward_badge': 'training_master_silver',
                'icon': '🏅'
            },
            {
                'id': 'department_war',
                'name': 'Department War',
                'description': 'Your department vs others - highest average score wins',
                'type': 'special',
                'duration_days': 30,
                'reward_points': 5000,
                'reward_badge': 'department_champion',
                'icon': '⚔️'
            },
            {
                'id': 'streak_defender',
                'name': 'Streak Defender',
                'description': 'Maintain a 30-day streak without any security incidents',
                'type': 'ongoing',
                'requirements': {'streak_days': 30},
                'reward_points': 3000,
                'reward_badge': 'vigilant_guardian_silver',
                'icon': '🔥'
            },
            {
                'id': 'phishing_hunter',
                'name': 'Phishing Hunter',
                'description': 'Report 10 suspicious emails this month',
                'type': 'monthly',
                'requirements': {'reports': 10},
                'reward_points': 1500,
                'reward_badge': 'phishing_spotter_silver',
                'icon': '🔍'
            }
        ]
    
    def _initialize_rewards(self) -> List[Dict]:
        """Initialize reward catalog"""
        return [
            {
                'id': 'reward_coffee',
                'name': '☕ Coffee Voucher',
                'description': 'Starbucks or local coffee shop voucher',
                'points_required': 1000,
                'type': 'voucher',
                'value': 5,
                'available': True
            },
            {
                'id': 'reward_lunch',
                'name': '🍱 Lunch Voucher',
                'description': 'Free lunch at company cafeteria',
                'points_required': 5000,
                'type': 'voucher',
                'value': 15,
                'available': True
            },
            {
                'id': 'reward_merch',
                'name': '👕 Security Merch',
                'description': 'Limited edition security t-shirt',
                'points_required': 10000,
                'type': 'merchandise',
                'available': True
            },
            {
                'id': 'reward_course',
                'name': '📚 Professional Course',
                'description': 'Paid cybersecurity certification course',
                'points_required': 50000,
                'type': 'education',
                'value': 500,
                'available': True
            },
            {
                'id': 'reward_phone',
                'name': '📱 Premium Phone',
                'description': 'Latest smartphone',
                'points_required': 250000,
                'type': 'electronics',
                'value': 1000,
                'available': True
            },
            {
                'id': 'reward_trip',
                'name': '✈️ Security Conference Trip',
                'description': 'All-expenses-paid trip to security conference',
                'points_required': 500000,
                'type': 'experience',
                'value': 5000,
                'available': True
            }
        ]
    
    def evaluate_achievements(self, user_data: Dict, db: Session) -> List[Dict]:
        """
        Evaluate and award new achievements
        """
        new_achievements = []
        
        for badge_id, badge in self.badges.items():
            current_tier = self._get_user_tier(user_data, badge_id)
            
            # Check each tier requirement
            for tier_idx, tier in enumerate(badge['tiers']):
                if tier_idx <= current_tier:  # Already earned
                    continue
                
                # Check requirements
                requirements_met = True
                for req_name, req_values in badge['requirements'].items():
                    user_value = user_data.get(req_name, 0)
                    required_value = req_values[tier_idx] if tier_idx < len(req_values) else req_values[-1]
                    
                    if user_value < required_value:
                        requirements_met = False
                        break
                
                if requirements_met:
                    new_achievements.append({
                        'badge_id': badge_id,
                        'tier': tier,
                        'name': badge['name'],
                        'points': badge['points'][tier_idx] if tier_idx < len(badge['points']) else badge['points'][-1],
                        'icon': badge['icon']
                    })
                    break  # Award highest tier achieved
        
        return new_achievements
    
    def _get_user_tier(self, user_data: Dict, badge_id: str) -> int:
        """Get current tier index for user's badge"""
        earned_badges = user_data.get('earned_badges', [])
        for badge in earned_badges:
            if badge['badge_id'] == badge_id:
                return badge['tier_index']
        return -1
    
    def calculate_level(self, total_points: int) -> Dict:
        """Calculate user level based on points"""
        for i, level in enumerate(reversed(self.levels)):
            if total_points >= level['min_points']:
                return {
                    'level': level['level'],
                    'name': level['name'],
                    'points_to_next': self._points_to_next_level(total_points, level['level']),
                    'benefits': level['benefits']
                }
        return self.levels[0]
    
    def _points_to_next_level(self, current_points: int, current_level: int) -> int:
        """Calculate points needed for next level"""
        if current_level >= len(self.levels):
            return 0
        
        next_level_points = self.levels[current_level]['min_points']
        return next_level_points - current_points
    
    def get_active_challenges(self, date: datetime = None) -> List[Dict]:
        """Get currently active challenges"""
        if date is None:
            date = datetime.now()
        
        active = []
        for challenge in self.challenges:
            if challenge['type'] == 'weekly':
                # Check if challenge is for current week
                if date.isocalendar()[1] % 4 == 0:  # Rotate weekly
                    active.append(challenge)
            elif challenge['type'] == 'monthly':
                # First week of month
                if date.day <= 7:
                    active.append(challenge)
            elif challenge['type'] == 'special':
                # Always active
                active.append(challenge)
            elif challenge['type'] == 'ongoing':
                active.append(challenge)
        
        return active
    
    def update_streak(self, user_id: int, db: Session) -> Dict:
        """Update and check user streak"""
        from models.gamification import UserStreak
        
        streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
        
        if not streak:
            streak = UserStreak(
                user_id=user_id,
                current_streak=1,
                longest_streak=1,
                last_activity=datetime.now()
            )
            db.add(streak)
            db.commit()
            return {'streak': 1, 'new_record': True}
        
        # Check if streak continues
        if streak.last_activity.date() == datetime.now().date() - timedelta(days=1):
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
                new_record = True
            else:
                new_record = False
        elif streak.last_activity.date() < datetime.now().date() - timedelta(days=1):
            # Streak broken
            streak.current_streak = 1
            new_record = False
        
       
