from typing import Dict, List, Any, Optional
import aiohttp
import asyncio
from datetime import datetime, timedelta
import hashlib
import hmac
import base64
import json
import logging
from sqlalchemy.orm import Session
from core.config import settings

logger = logging.getLogger(__name__)

class HRISIntegration:
    """
    Integration with HR Information Systems
    """
    
    def __init__(self):
        self.providers = {
            'workday': self._sync_workday,
            'successfactors': self._sync_successfactors,
            'bamboo': self._sync_bamboo,
            'adp': self._sync_adp,
            'oracle_hcm': self._sync_oracle_hcm
        }
    
    async def sync_employees(
        self,
        provider: str,
        api_key: str,
        api_secret: str,
        instance_url: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Sync employee data from HRIS
        """
        if provider not in self.providers:
            raise ValueError(f"Unsupported HRIS provider: {provider}")
        
        sync_func = self.providers[provider]
        return await sync_func(api_key, api_secret, instance_url, db)
    
    async def _sync_workday(
        self,
        api_key: str,
        api_secret: str,
        instance_url: str,
        db: Session
    ) -> Dict[str, Any]:
        """Sync with Workday"""
        
        from models.user import User
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Workday API endpoint for employee data
        url = f"{instance_url}/api/v1/workers"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Workday sync failed: {response.status}")
                    return {'success': False, 'error': 'API connection failed'}
                
                data = await response.json()
                
        # Process and upsert employees
        stats = {'added': 0, 'updated': 0, 'deactivated': 0, 'errors': 0}
        
        for worker in data.get('workers', []):
            try:
                email = worker.get('email')
                if not email:
                    continue
                
                # Check if user exists
                user = db.query(User).filter(User.email == email).first()
                
                if user:
                    # Update existing user
                    user.full_name = f"{worker.get('first_name')} {worker.get('last_name')}"
                    user.department = worker.get('department')
                    user.job_title = worker.get('job_title')
                    user.manager_email = worker.get('manager_email')
                    user.employment_status = worker.get('status', 'active')
                    user.hire_date = worker.get('hire_date')
                    user.employee_id = worker.get('employee_id')
                    
                    if worker.get('status') != 'active':
                        user.is_active = False
                        stats['deactivated'] += 1
                    else:
                        stats['updated'] += 1
                else:
                    # Create new user
                    user = User(
                        email=email,
                        username=email.split('@')[0],
                        full_name=f"{worker.get('first_name')} {worker.get('last_name')}",
                        department=worker.get('department'),
                        job_title=worker.get('job_title'),
                        manager_email=worker.get('manager_email'),
                        employee_id=worker.get('employee_id'),
                        hire_date=worker.get('hire_date'),
                        is_active=(worker.get('status') == 'active'),
                        source='hris_sync'
                    )
                    db.add(user)
                    stats['added'] += 1
                
            except Exception as e:
                logger.error(f"Error processing worker: {e}")
                stats['errors'] += 1
        
        db.commit()
        
        return {
            'success': True,
            'provider': 'workday',
            'timestamp': datetime.now().isoformat(),
            'stats': stats
        }
    
    async def _sync_successfactors(
        self,
        api_key: str,
        api_secret: str,
        instance_url: str,
        db: Session
    ) -> Dict[str, Any]:
        """Sync with SAP SuccessFactors"""
        # Similar implementation for SuccessFactors
        pass
    
    async def get_organization_chart(self, db: Session) -> Dict[str, Any]:
        """
        Build organization chart from HR data
        """
        from models.user import User
        
        users = db.query(User).filter(User.is_active == True).all()
        
        # Build hierarchy
        org_chart = {}
        managers = {}
        
        for user in users:
            if user.manager_email:
                if user.manager_email not in managers:
                    managers[user.manager_email] = []
                managers[user.manager_email].append({
                    'id': user.id,
                    'name': user.full_name,
                    'email': user.email,
                    'department': user.department,
                    'job_title': user.job_title,
                    'risk_score': user.risk_score
                })
        
        # Find top-level managers (no manager or manager not in system)
        top_level = []
        for user in users:
            if not user.manager_email or user.manager_email not in [u.email for u in users]:
                top_level.append({
                    'id': user.id,
                    'name': user.full_name,
                    'email': user.email,
                    'department': user.department,
                    'job_title': user.job_title,
                    'risk_score': user.risk_score,
                    'direct_reports': managers.get(user.email, [])
                })
        
        return {
            'total_employees': len(users),
            'top_managers': top_level,
            'org_structure': managers
        }

class SIEMIntegration:
    """
    Integration with Security Information and Event Management systems
    """
    
    def __init__(self):
        self.siem_providers = {
            'splunk': self._send_to_splunk,
            'qradar': self._send_to_qradar,
            'arcsight': self._send_to_arcsight,
            'logrhythm': self._send_to_logrhythm,
            'elastic': self._send_to_elastic,
            'azure_sentinel': self._send_to_azure_sentinel,
            'aws_cloudwatch': self._send_to_cloudwatch
        }
    
    async def send_security_event(
        self,
        provider: str,
        event_type: str,
        event_data: Dict[str, Any],
        severity: str = 'info'
    ) -> bool:
        """
        Send security event to SIEM
        """
        if provider not in self.siem_providers:
            logger.error(f"Unsupported SIEM provider: {provider}")
            return False
        
        # Enrich event with common fields
        enriched_event = {
            'timestamp': datetime.now().isoformat(),
            'source': 'phishing_simulation_platform',
            'event_type': event_type,
            'severity': severity,
            'data': event_data
        }
        
        send_func = self.siem_providers[provider]
        return await send_func(enriched_event)
    
    async def _send_to_splunk(self, event: Dict[str, Any]) -> bool:
        """Send event to Splunk HEC"""
        
        url = settings.SPLUNK_HEC_URL
        token = settings.SPLUNK_HEC_TOKEN
        
        headers = {
            'Authorization': f'Splunk {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'event': event,
            'sourcetype': 'phishing_simulation',
            'source': 'security_awareness',
            'host': 'phishing-platform'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        logger.info("Event sent to Splunk successfully")
                        return True
                    else:
                        logger.error(f"Splunk error: {response.status}")
                        return False
            except Exception as e:
                logger.error(f"Failed to send to Splunk: {e}")
                return False
    
    async def _send_to_azure_sentinel(self, event: Dict[str, Any]) -> bool:
        """Send event to Azure Sentinel"""
        
        workspace_id = settings.AZURE_WORKSPACE_ID
        shared_key = settings.AZURE_SHARED_KEY
        
        # Generate signature
        body = json.dumps(event)
        content_length = len(body)
        rfc1123date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        string_to_hash = f'POST\n{content_length}\napplication/json\nx-ms-date:{rfc1123date}\n/api/logs'
        
        bytes_to_hash = string_to_hash.encode('utf-8')
        decoded_key = base64.b64decode(shared_key)
        
        encoded_hash = base64.b64encode(
            hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
        ).decode()
        
        authorization = f'SharedKey {workspace_id}:{encoded_hash}'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': authorization,
            'Log-Type': 'PhishingSimulation',
            'x-ms-date': rfc1123date,
            'time-generated-field': 'timestamp'
        }
        
        url = f"https://{workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, data=body) as response:
                    if response.status == 200:
                        logger.info("Event sent to Azure Sentinel")
                        return True
                    else:
                        logger.error(f"Azure error: {response.status}")
                        return False
            except Exception as e:
                logger.error(f"Failed to send to Azure: {e}")
                return False
    
    async def forward_alerts_to_siem(
        self,
        alert_data: Dict[str, Any],
        providers: List[str] = None
    ) -> Dict[str, bool]:
        """
        Forward security alerts to multiple SIEMs
        """
        if providers is None:
            providers = ['splunk', 'azure_sentinel']
        
        results = {}
        tasks = []
        
        for provider in providers:
            if provider in self.siem_providers:
                task = self.send_security_event(
                    provider,
                    'security_alert',
                    alert_data,
                    severity=alert_data.get('severity', 'high')
                )
                tasks.append((provider, task))
        
        # Execute all sends concurrently
        for provider, task in tasks:
            results[provider] = await task
        
        return results

class APIGatewayIntegration:
    """
    Integration with API Gateway for microservices architecture
    """
    
    def __init__(self):
        self.services = {
            'user_service': 'http://user-service:8001',
            'training_service': 'http://training-service:8002',
            'analytics_service': 'http://analytics-service:8003',
            'notification_service': 'http://notification-service:8004'
        }
    
    async def register_service(self, service_name: str, service_url: str):
        """Register a microservice"""
        self.services[service_name] = service_url
        logger.info(f"Registered service: {service_name}")
    
    async def call_service(
        self,
        service_name: str,
        endpoint: str,
        method: str = 'GET',
        data: Dict = None
    ) -> Dict[str, Any]:
        """Call another microservice"""
        
        if service_name not in self.services:
            raise ValueError(f"Unknown service: {service_name}")
        
        url = f"{self.services[service_name]}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            if method.upper() == 'GET':
                async with session.get(url) as response:
                    return await response.json()
            elif method.upper() == 'POST':
                async with session.post(url, json=data) as response:
                    return await response.json()
            elif method.upper() == 'PUT':
                async with session.put(url, json=data) as response:
                    return await response.json()

# Initialize integration services
hris_integration = HRISIntegration()
siem_integration = SIEMIntegration()
api_gateway = APIGatewayIntegration()
