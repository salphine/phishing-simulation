from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class EmailEvent(Base):
    __tablename__ = "email_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, index=True)
    email_id = Column(String(200), index=True)
    event_type = Column(String(50))  # sent, opened, clicked, bounced, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    event_metadata = Column(Text, nullable=True)  # Changed from 'metadata' to 'event_metadata'
    
    def __repr__(self):
        return f"<EmailEvent {self.event_type} for user {self.user_id}>"
