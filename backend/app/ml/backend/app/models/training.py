from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class TrainingAssignment(Base):
    __tablename__ = "training_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    training_name = Column(String(200))
    training_type = Column(String(100))
    assigned_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, overdue
    score = Column(Float, nullable=True)
    passed = Column(Boolean, nullable=True)
    progress = Column(Integer, default=0)  # 0-100
    
    def __repr__(self):
        return f"<TrainingAssignment {self.training_name} for user {self.user_id}>"
