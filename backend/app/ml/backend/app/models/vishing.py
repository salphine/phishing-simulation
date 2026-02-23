from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class VishingCampaign(Base):
    __tablename__ = "vishing_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(Text)
    script = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    def __repr__(self):
        return f"<VishingCampaign {self.name}>"

class VishingCall(Base):
    __tablename__ = "vishing_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, ForeignKey("vishing_campaigns.id"))
    phone_number = Column(String(20))
    call_sid = Column(String(200), unique=True)
    call_time = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer, default=0)  # in seconds
    recording_url = Column(String(500), nullable=True)
    transcription = Column(Text, nullable=True)
    analysis_result = Column(Text, nullable=True)  # JSON string
    risk_score = Column(Float, nullable=True)
    status = Column(String(50), default="initiated")  # initiated, completed, failed
    
    def __repr__(self):
        return f"<VishingCall {self.id} for user {self.user_id}>"
