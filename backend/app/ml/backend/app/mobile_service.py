from typing import Dict, List, Any
import aiohttp
import asyncio
from datetime import datetime
import logging
from core.config import settings

logger = logging.getLogger(__name__)

class MobilePushService:
    """
    Mobile push notification service for iOS and Android
    """
    
    def __init__(self):
        self.fcm_api_key = settings.FCM_API_KEY
        self.apns_key = settings.APNS_KEY
        self.apns_key_id = settings.APNS_KEY_ID
        self.apns_team_id = settings.APNS_TEAM_ID
        self.apns_topic = settings.APNS_TOPIC
        
    async def send_push_notification(
        self,
        device_token: str,
        platform: str,  # 'ios' or 'android'
        title: str,
        body: str,
        data: Dict[str, Any] = None,
        sound: str = "default",
        badge: int = None
    ):
        """
        Send push notification to specific device
        """
        if platform == 'android':
            return await self._send_fcm_notification(
                device_token, title, body, data, sound, badge
            )
        elif platform == 'ios':
            return await self._send_apns_notification(
                device_token, title, body, data, sound, badge
            )
        else:
            logger.error(f"Unknown platform: {platform}")
            return False
    
    async def _send_fcm_notification(
        self,
        token: str,
        title: str,
        body: str,
        data: Dict = None,
        sound: str = "default",
        badge: int = None
    ):
        """Send Android notification via FCM"""
        
        url = "https://fcm.googleapis.com/fcm/send"
        
        headers = {
            "Authorization": f"key={self.fcm_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "to": token,
            "notification": {
                "title": title,
                "body": body,
                "sound": sound,
                "badge": badge if badge else 1,
                "click_action": "OPEN_ACTIVITY"
            },
            "data": data or {},
            "priority": "high"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"FCM notification sent: {result}")
                    return result.get("success", 0) == 1
                else:
                    logger.error(f"FCM error: {response.status}")
                    return False
    
    async def _send_apns_notification(
        self,
        token: str,
        title: str,
        body: str,
        data: Dict = None,
        sound: str = "default",
        badge: int = None
    ):
        """Send iOS notification via APNS"""
        
        # Generate JWT token for APNS
        import jwt
        import time
        
        # Create JWT
        claims = {
            'iss': self.apns_team_id,
            'iat': int(time.time())
        }
        
        jwt_token = jwt.encode(
            claims,
            self.apns_key,
            algorithm='ES256',
            headers={
                'alg': 'ES256',
                'kid': self.apns_key_id
            }
        )
        
        # APNS request
        url = f"https://api.push.apple.com/3/device/{token}"
        
        headers = {
            "Authorization": f"bearer {jwt_token}",
            "apns-topic": self.apns_topic,
            "apns-push-type": "alert",
            "apns-priority": "10"
        }
        
        payload = {
            "aps": {
                "alert": {
                    "title": title,
                    "body": body
                },
                "sound": sound,
                "badge": badge if badge else 1,
                "content-available": 1
            },
            "data": data or {}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    logger.info(f"APNS notification sent")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"APNS error: {response.status} - {error}")
                    return False
    
    async def send_bulk_notifications(
        self,
        devices: List[Dict],
        title: str,
        body: str,
        data: Dict = None
    ) -> Dict:
        """
        Send notifications to multiple devices
        """
        tasks = []
        for device in devices:
            tasks.append(
                self.send_push_notification(
                    device['token'],
                    device['platform'],
                    title,
                    body,
                    data
                )
            )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if r is True)
        failure_count = sum(1 for r in results if r is False)
        
        return {
            'total': len(devices),
            'success': success_count,
            'failure': failure_count
        }

class MobileAPIService:
    """
    Mobile-specific API endpoints and business logic
    """
    
    async def get_mobile_dashboard(self, user_id: int, db) -> Dict:
        """
        Get mobile-optimized dashboard data
        """
        from models.user import User
        from models.campaign import EmailEvent
        from models.gamification import UserPoints, UserBadge, UserStreak
        
        user = db.query(User).get(user_id)
        
        # Get recent activity
        recent_activity = db.query(EmailEvent).filter(
            EmailEvent.user_id == user_id
        ).order_by(EmailEvent.sent_at.desc()).limit(10).all()
        
        # Get gamification data
        points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
        badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).count()
        streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
        
        # Calculate risk score trend
        risk_history = [
            {
                'date': event.sent_at,
                'clicked': event.clicked_at is not None
            }
            for event in recent_activity
        ]
        
        return {
            'user': {
                'name': user.full_name,
                'department': user.department,
                'risk_score': user.risk_score
            },
            'gamification': {
                'points': points.total_points if points else 0,
                'badges': badges,
                'streak': streak.current_streak if streak else 0,
                'level': gamification_service.calculate_level(points.total_points if points else 0)
            },
            'recent_activity': [
                {
                    'date': a.sent_at.isoformat(),
                    'type': 'phishing_simulation' if a.campaign_id else 'training',
                    'result': 'clicked' if a.clicked_at else 'ignored'
                }
                for a in recent_activity
            ],
            'risk_trend': risk_history,
            'next_training': await self._get_next_training(user_id, db)
        }
    
    async def _get_next_training(self, user_id: int, db) -> Dict:
        """Get next recommended training for mobile"""
        from models.training import TrainingAssignment
        
        pending = db.query(TrainingAssignment).filter(
            TrainingAssignment.user_id == user_id,
            TrainingAssignment.completed_at == None
        ).first()
        
        if pending:
            return {
                'id': pending.id,
                'module': pending.module.name,
                'due_date': pending.assigned_at + timedelta(days=7),
                'type': 'mandatory'
            }
        
        return None
    
    async def quick_training_session(self, user_id: int, duration_minutes: int = 5) -> Dict:
        """
        Generate a quick 5-minute mobile training session
        """
        # Get user's weak areas
        weak_areas = await self._identify_weak_areas(user_id)
        
        # Generate micro-learning content
        training_content = {
            'duration': duration_minutes,
            'sections': []
        }
        
        for area in weak_areas[:3]:  # Top 3 weak areas
            section = {
                'topic': area['topic'],
                'content': await self._get_micro_content(area['topic']),
                'quiz': await self._generate_quick_quiz(area['topic']),
                'estimated_time': duration_minutes // 3
            }
            training_content['sections'].append(section)
        
        return training_content
    
    async def _identify_weak_areas(self, user_id: int) -> List[Dict]:
        """Identify user's weak areas for targeted training"""
        # This would use ML predictions to identify weak spots
        return [
            {'topic': 'link_verification', 'score': 65},
            {'topic': 'attachment_safety', 'score': 70},
            {'topic': 'urgency_recognition', 'score': 45}
        ]
    
    async def _get_micro_content(self, topic: str) -> str:
        """Get micro-learning content for topic"""
        content_map = {
            'link_verification': 'Always hover over links to see the real URL before clicking...',
            'attachment_safety': 'Never open unexpected attachments, even from known senders...',
            'urgency_recognition': 'Phishing emails often create false urgency to rush your decision...'
        }
        return content_map.get(topic, 'General security tip')
    
    async def _generate_quick_quiz(self, topic: str) -> Dict:
        """Generate a quick quiz question"""
        return {
            'question': 'What should you do before clicking a link in an email?',
            'options': [
                'Click immediately',
                'Hover to check the URL',
                'Forward to friends',
                'Download attachment first'
            ],
            'correct': 1,
            'explanation': 'Always verify the destination URL by hovering over the link.'
        }

mobile_api_service = MobileAPIService()
mobile_push_service = MobilePushService()
