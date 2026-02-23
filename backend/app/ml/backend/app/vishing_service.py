import asyncio
import aiohttp
from typing import Dict, List, Any
from datetime import datetime
import logging
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import boto3
from core.config import settings

logger = logging.getLogger(__name__)

class VishingService:
    """
    Voice Phishing (Vishing) Simulation Service
    """
    
    def __init__(self):
        # Twilio for calls
        self.twilio_client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.twilio_phone = settings.TWILIO_PHONE_NUMBER
        
        # AWS Polly for voice synthesis
        self.polly_client = boto3.client(
            'polly',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        # Voice scripts by scenario
        self.scripts = self._initialize_scripts()
        
    def _initialize_scripts(self) -> Dict[str, Dict]:
        """Initialize vishing scripts for different scenarios"""
        return {
            'tech_support': {
                'name': 'Fake Tech Support',
                'greeting': 'Hello, this is John from IT Support. We\'ve detected a virus on your computer.',
                'script': [
                    'We need you to install a security update immediately.',
                    'Please visit {link} and enter your credentials.',
                    'This is urgent to prevent data loss.'
                ],
                'questions': {
                    'verify_identity': 'Can you confirm your employee ID?',
                    'remote_access': 'We need remote access to fix this.',
                    'credentials': 'What\'s your current password?'
                },
                'red_flags': [
                    'Unsolicited tech support call',
                    'Urgency to act immediately',
                    'Request for credentials',
                    'Request for remote access'
                ],
                'training_module': 'vishing_tech_support'
            },
            'bank_fraud': {
                'name': 'Bank Security Alert',
                'greeting': 'This is the fraud department at {bank_name}. We\'ve detected suspicious activity.',
                'script': [
                    'Someone tried to transfer ${amount} from your account.',
                    'To stop this transaction, we need to verify your identity.',
                    'Please confirm the code we\'re sending to your phone.'
                ],
                'questions': {
                    'verify_card': 'Please read your card number.',
                    'verify_code': 'What\'s the verification code we sent?',
                    'transfer_approve': 'To approve the transfer, press 1.'
                },
                'red_flags': [
                    'Caller asks for card details',
                    'Urgent threats about account closure',
                    'Requests verification codes',
                    'Pressure to act quickly'
                ],
                'training_module': 'vishing_bank_fraud'
            },
            'hr_benefits': {
                'name': 'HR Benefits Update',
                'greeting': 'This is HR regarding your benefits enrollment.',
                'script': [
                    'Open enrollment ends today.',
                    'Click the link we\'ll text you to update your information.',
                    'Failure to update may result in loss of benefits.'
                ],
                'questions': {
                    'ssn': 'We need your SSN for verification.',
                    'dob': 'Please confirm your date of birth.',
                    'employee_id': 'What\'s your employee ID?'
                },
                'red_flags': [
                    'Requests for personal information',
                    'Threats of losing benefits',
                    'Unsolicited HR calls',
                    'Requests via text after call'
                ],
                'training_module': 'vishing_hr_scam'
            },
            'ceo_fraud': {
                'name': 'CEO Impersonation',
                'greeting': 'Hi {employee_name}, this is {ceo_name}, the CEO.',
                'script': [
                    'I need your help with an urgent matter.',
                    'I\'m in a meeting and need you to purchase gift cards.',
                    'I\'ll text you the details. Keep this confidential.'
                ],
                'questions': {
                    'amount': 'How many cards can you get right now?',
                    'codes': 'Read me the codes from the back.',
                    'confidential': 'This stays between us, okay?'
                },
                'red_flags': [
                    'Unexpected call from executive',
                    'Request for gift cards',
                    'Pressure for confidentiality',
                    'Unusual payment requests'
                ],
                'training_module': 'vishing_ceo_fraud'
            }
        }
    
    async def initiate_vishing_call(
        self,
        phone_number: str,
        scenario: str,
        employee_name: str,
        employee_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Initiate a vishing simulation call
        """
        try:
            # Get script
            script = self.scripts.get(scenario, self.scripts['tech_support'])
            
            # Personalize script
            personalized_script = self._personalize_script(
                script,
                employee_name,
                employee_data
            )
            
            # Generate TwiML for the call
            twiml = self._generate_twiml(personalized_script, scenario)
            
            # Make the call
            call = self.twilio_client.calls.create(
                twiml=twiml,
                to=phone_number,
                from_=self.twilio_phone,
                status_callback=f"{settings.BASE_URL}/api/vishing/callback",
                status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
                status_callback_method='POST'
            )
            
            logger.info(f"Vishing call initiated: {call.sid} to {phone_number}")
            
            return {
                'call_sid': call.sid,
                'status': call.status,
                'scenario': scenario,
                'start_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Vishing call failed: {e}")
            raise
    
    def _personalize_script(
        self,
        script: Dict,
        employee_name: str,
        employee_data: Dict
    ) -> Dict:
        """Personalize script with employee data"""
        
        personalized = script.copy()
        
        # Replace placeholders
        personalized['greeting'] = script['greeting'].format(
            employee_name=employee_name,
            ceo_name=employee_data.get('ceo_name', 'Mr. Smith'),
            bank_name=employee_data.get('bank_name', 'Your Bank'),
            amount=employee_data.get('amount', '500')
        )
        
        personalized['script'] = [
            line.format(
                link=employee_data.get('link', 'secure-update.com'),
                amount=employee_data.get('amount', '500')
            )
            for line in script['script']
        ]
        
        return personalized
    
    def _generate_twiml(self, script: Dict, scenario: str) -> str:
        """Generate TwiML for the call"""
        
        response = VoiceResponse()
        
        # Greeting
        response.say(script['greeting'], voice='Polly.Joanna')
        
        # Main script with pauses
        for line in script['script']:
            response.pause(length=1)
            response.say(line, voice='Polly.Joanna')
        
        # Interactive questions
        gather = Gather(
            input='dtmf speech',
            timeout=5,
            num_digits=1,
            action=f'/api/vishing/handle-response/{scenario}',
            method='POST'
        )
        
        for question in script['questions'].values():
            gather.say(question, voice='Polly.Joanna')
            gather.pause(length=2)
        
        response.append(gather)
        
        # If no input
        response.say(
            "We didn't receive your response. Please call our security team if you have concerns.",
            voice='Polly.Joanna'
        )
        
        return str(response)
    
    async def generate_voice_audio(self, text: str, voice_id: str = 'Joanna') -> bytes:
        """Generate audio file using AWS Polly"""
        
        response = self.polly_client.synthesize_speech(
            Engine='neural',
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id
        )
        
        return response['AudioStream'].read()
    
    async def analyze_call_response(
        self,
        call_sid: str,
        user_response: str,
        scenario: str
    ) -> Dict[str, Any]:
        """Analyze user's response to vishing call"""
        
        # Check if user fell for the vishing
        fell_for_it = self._check_if_fell_for_it(user_response, scenario)
        
        # Determine appropriate training
        if fell_for_it:
            training_module = self.scripts[scenario]['training_module']
            
            # Log the incident
            logger.warning(f"User fell for vishing: {call_sid}, scenario: {scenario}")
            
            return {
                'vulnerable': True,
                'training_needed': training_module,
                'severity': 'high',
                'response_analysis': {
                    'provided_info': user_response,
                    'red_flags_ignored': self.scripts[scenario]['red_flags']
                }
            }
        else:
            # User correctly identified the vishing
            return {
                'vulnerable': False,
                'training_needed': None,
                'severity': 'low',
                'response_analysis': {
                    'correct_action': 'Did not provide sensitive information',
                    'commendation': 'Good security awareness!'
                }
            }
    
    def _check_if_fell_for_it(self, response: str, scenario: str) -> bool:
        """Check if user fell for the vishing attempt"""
        
        # This would use NLP/ML in production
        # Simple keyword-based check for demo
        sensitive_keywords = [
            'password', 'credit card', 'ssn', 'social security',
            'code', 'verify', 'yes', 'okay', 'sure'
        ]
        
        response_lower = response.lower()
        
        for keyword in sensitive_keywords:
            if keyword in response_lower:
                return True
        
        return False
    
    async def process_callback(self, data: Dict) -> None:
        """Process Twilio callback events"""
        
        call_sid = data.get('CallSid')
        call_status = data.get('CallStatus')
        duration = data.get('CallDuration')
        
        logger.info(f"Vishing call {call_sid} status: {call_status}, duration: {duration}s")
        
        # Update database with call results
        # This would update the user's record and trigger training if needed

class VishingAnalytics:
    """
    Analytics for vishing campaigns
    """
    
    def analyze_campaign_results(self, calls: List[Dict]) -> Dict[str, Any]:
        """Analyze vishing campaign results"""
        
        total_calls = len(calls)
        answered = sum(1 for c in calls if c.get('answered', False))
        fell_for = sum(1 for c in calls if c.get('fell_for', False))
        
        return {
            'total_calls': total_calls,
            'answer_rate': (answered / total_calls * 100) if total_calls > 0 else 0,
            'vulnerability_rate': (fell_for / answered * 100) if answered > 0 else 0,
            'average_duration': sum(c.get('duration', 0) for c in calls) / total_calls if total_calls > 0 else 0,
            'by_scenario': self._analyze_by_scenario(calls),
            'by_department': self._analyze_by_department(calls),
            'risk_trend': self._calculate_risk_trend(calls)
        }
    
    def _analyze_by_scenario(self, calls: List[Dict]) -> Dict[str, Any]:
        """Analyze results by vishing scenario"""
        
        scenarios = {}
        for call in calls:
            scenario = call.get('scenario', 'unknown')
            if scenario not in scenarios:
                scenarios[scenario] = {
                    'total': 0,
                    'fell_for': 0,
                    'duration_sum': 0
                }
            
            scenarios[scenario]['total'] += 1
            if call.get('fell_for'):
                scenarios[scenario]['fell_for'] += 1
            scenarios[scenario]['duration_sum'] += call.get('duration', 0)
        
        # Calculate percentages
        for scenario, data in scenarios.items():
            data['vulnerability_rate'] = (
                data['fell_for'] / data['total'] * 100
            ) if data['total'] > 0 else 0
            data['avg_duration'] = (
                data['duration_sum'] / data['total']
            ) if data['total'] > 0 else 0
        
        return scenarios
    
    def _analyze_by_department(self, calls: List[Dict]) -> Dict[str, Any]:
        """Analyze results by department"""
        
        departments = {}
        for call in calls:
            dept = call.get('department', 'unknown')
            if dept not in departments:
                departments[dept] = {
                    'total': 0,
                    'fell_for': 0,
                    'users': set()
                }
            
            departments[dept]['total'] += 1
            if call.get('fell_for'):
                departments[dept]['fell_for'] += 1
            departments[dept]['users'].add(call.get('user_id'))
        
        # Calculate risk scores
        for dept, data in departments.items():
            data['vulnerability_rate'] = (
                data['fell_for'] / data['total'] * 100
            ) if data['total'] > 0 else 0
            data['unique_users'] = len(data['users'])
            data['risk_score'] = self._calculate_department_risk(data)
            del data['users']
        
        return departments
    
    def _calculate_department_risk(self, data: Dict) -> int:
        """Calculate risk score for department"""
        
        # Weighted risk calculation
        vulnerability_weight = data.get('vulnerability_rate', 0) * 0.6
        volume_weight = min(data.get('total', 0) / 100, 1) * 0.4
        
        return int(vulnerability_weight + volume_weight * 100)
    
    def _calculate_risk_trend(self, calls: List[Dict]) -> List[Dict]:
        """Calculate risk trend over time"""
        
        # Group by date
        from collections import defaultdict
        daily = defaultdict(lambda: {'total': 0, 'fell_for': 0})
        
        for call in calls:
            date = call.get('date', datetime.now().date())
            daily[date]['total'] += 1
            if call.get('fell_for'):
                daily[date]['fell_for'] += 1
        
        # Calculate rates
        trend = []
        for date in sorted(daily.keys()):
            data = daily[date]
            trend.append({
                'date': date.isoformat(),
                'vulnerability_rate': (
                    data['fell_for'] / data['total'] * 100
                ) if data['total'] > 0 else 0,
                'call_volume': data['total']
            })
        
        return trend

# Initialize services
vishing_service = VishingService()
vishing_analytics = VishingAnalytics()
