from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class BlockchainRecord(Base):
    __tablename__ = "blockchain_records"

    id = Column(Integer, primary_key=True, index=True)
    training_assignment_id = Column(Integer, ForeignKey("training_assignments.id"), unique=True, nullable=True)
    
    # Blockchain data
    record_hash = Column(String(200), unique=True, index=True)
    tx_hash = Column(String(200), unique=True)
    block_number = Column(Integer)
    block_timestamp = Column(DateTime, nullable=True)

    # Record data
    user_id = Column(Integer, ForeignKey("users.id"))
    module_id = Column(Integer, ForeignKey("training_modules.id"), nullable=True)
    score = Column(Float, nullable=True)
    record_metadata = Column(JSON, default={})

    # Verification
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    training_assignment = relationship("TrainingAssignment", backref="blockchain_record", foreign_keys=[training_assignment_id])
    user = relationship("User", foreign_keys=[user_id])
    module = relationship("TrainingModule", foreign_keys=[module_id])
    
    def __repr__(self):
        return f"<BlockchainRecord {self.tx_hash}>"

class BlockchainVerification(Base):
    __tablename__ = "blockchain_verifications"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("blockchain_records.id"))
    verifier_address = Column(String(200))
    verification_hash = Column(String(200), unique=True)
    verified = Column(Boolean, default=False)

    verified_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    record = relationship("BlockchainRecord", backref="verifications")
    
    def __repr__(self):
        return f"<BlockchainVerification {self.verification_hash}>"

class AuditReport(Base):
    __tablename__ = "audit_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(100), unique=True, index=True)
    report_type = Column(String(50))  # 'compliance', 'training', 'security'
    department = Column(String(100), nullable=True)

    # Report data
    report_data = Column(JSON)
    merkle_root = Column(String(200), nullable=True)

    # Status
    status = Column(String(50), default="generated")
    downloaded = Column(Boolean, default=False)

    # Timestamps
    generated_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)

    # Audit trail
    generated_by = Column(Integer, ForeignKey("users.id"))
    generator = relationship("User", foreign_keys=[generated_by])
    
    def __repr__(self):
        return f"<AuditReport {self.report_id}>"
