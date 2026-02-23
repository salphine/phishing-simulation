from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class HRISSync(Base):
    __tablename__ = "hris_sync"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(100), unique=True, index=True)
    employee_name = Column(String(200))
    department = Column(String(100))
    position = Column(String(100))
    email = Column(String(200))
    hire_date = Column(DateTime)
    last_sync = Column(DateTime, default=datetime.utcnow)
    sync_status = Column(String(50), default="pending")
    sync_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<HRISSync {self.employee_id}>"

class SIEMConfig(Base):
    __tablename__ = "siem_config"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    endpoint = Column(String(500))
    api_key = Column(String(500))
    api_secret = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    config = Column(JSON, default={})
    
    def __repr__(self):
        return f"<SIEMConfig {self.name}>"

class Webhook(Base):
    __tablename__ = "webhooks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    url = Column(String(500))
    secret = Column(String(500), nullable=True)
    events = Column(JSON, default=[])  # List of events to trigger on
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_triggered = Column(DateTime, nullable=True)
    failure_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Webhook {self.name}>"
