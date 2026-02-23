from web3 import Web3
from eth_account import Account
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import hashlib
import logging
from sqlalchemy.orm import Session
from core.config import settings

logger = logging.getLogger(__name__)

class BlockchainAuditService:
    """
    Blockchain-based immutable audit trail for training records
    """
    
    def __init__(self):
        # Connect to blockchain (Ethereum, Hyperledger, or local testnet)
        self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
        self.chain_id = settings.BLOCKCHAIN_CHAIN_ID
        
        # Load contract
        self.contract_address = settings.BLOCKCHAIN_CONTRACT_ADDRESS
        self.contract_abi = self._load_contract_abi()
        
        # Initialize account
        self.account = Account.from_key(settings.BLOCKCHAIN_PRIVATE_KEY)
        
        # Initialize contract
        if self.contract_address and self.contract_abi:
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=self.contract_abi
            )
        else:
            self.contract = None
            logger.warning("Blockchain contract not configured")
    
    def _load_contract_abi(self) -> List:
        """Load contract ABI from file"""
        try:
            with open('blockchain/contracts/TrainingAudit.json', 'r') as f:
                contract_data = json.load(f)
                return contract_data['abi']
        except:
            # Return minimal ABI for testing
            return [
                {
                    "inputs": [
                        {"internalType": "string", "name": "recordHash", "type": "string"},
                        {"internalType": "string", "name": "metadata", "type": "string"}
                    ],
                    "name": "storeRecord",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [{"internalType": "string", "name": "recordHash", "type": "string"}],
                    "name": "getRecord",
                    "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
    
    def create_record_hash(self, record_data: Dict) -> str:
        """
        Create cryptographic hash of record data
        """
        # Sort keys for consistent hashing
        record_string = json.dumps(record_data, sort_keys=True)
        
        # Create SHA-256 hash
        record_hash = hashlib.sha256(record_string.encode()).hexdigest()
        
        return record_hash
    
    async def store_training_record(
        self,
        user_id: int,
        training_id: int,
        module_name: str,
        score: float,
        completion_date: datetime,
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """
        Store training completion record on blockchain
        """
        
        # Create record data
        record_data = {
            'user_id': user_id,
            'training_id': training_id,
            'module_name': module_name,
            'score': score,
            'completion_date': completion_date.isoformat(),
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Create hash
        record_hash = self.create_record_hash(record_data)
        
        # Store on blockchain
        blockchain_tx = None
        if self.contract:
            try:
                # Build transaction
                tx = self.contract.functions.storeRecord(
                    record_hash,
                    json.dumps(record_data)
                ).build_transaction({
                    'from': self.account.address,
                    'nonce': self.w3.eth.get_transaction_count(self.account.address),
                    'gas': 2000000,
                    'gasPrice': self.w3.eth.gas_price
                })
                
                # Sign transaction
                signed_tx = self.account.sign_transaction(tx)
                
                # Send transaction
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                
                # Wait for receipt
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
                
                blockchain_tx = {
                    'tx_hash': tx_hash.hex(),
                    'block_number': receipt['blockNumber'],
                    'gas_used': receipt['gasUsed']
                }
                
                logger.info(f"Training record stored on blockchain: {tx_hash.hex()}")
                
            except Exception as e:
                logger.error(f"Failed to store on blockchain: {e}")
        
        return {
            'record_hash': record_hash,
            'record_data': record_data,
            'blockchain': blockchain_tx,
            'timestamp': datetime.now().isoformat()
        }
    
    async def verify_training_record(
        self,
        record_hash: str,
        expected_data: Dict = None
    ) -> Dict[str, Any]:
        """
        Verify training record on blockchain
        """
        
        verification = {
            'record_hash': record_hash,
            'exists_on_blockchain': False,
            'matches_expected': None,
            'blockchain_data': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Check on blockchain
        if self.contract:
            try:
                blockchain_data = self.contract.functions.getRecord(record_hash).call()
                
                if blockchain_data:
                    verification['exists_on_blockchain'] = True
                    verification['blockchain_data'] = json.loads(blockchain_data)
                    
                    # Verify against expected data
                    if expected_data:
                        expected_hash = self.create_record_hash(expected_data)
                        verification['matches_expected'] = (expected_hash == record_hash)
                        
            except Exception as e:
                logger.error(f"Failed to verify on blockchain: {e}")
        
        return verification
    
    async def get_user_training_history(self, user_id: int, db: Session) -> List[Dict]:
        """
        Get user's training history with blockchain verification
        """
        from models.training import TrainingAssignment
        from models.blockchain import BlockchainRecord
        
        assignments = db.query(TrainingAssignment).filter(
            TrainingAssignment.user_id == user_id,
            TrainingAssignment.completed_at.isnot(None)
        ).all()
        
        history = []
        for assignment in assignments:
            # Get blockchain record
            blockchain_record = db.query(BlockchainRecord).filter(
                BlockchainRecord.training_assignment_id == assignment.id
            ).first()
            
            record = {
                'training_id': assignment.id,
                'module_name': assignment.module.name,
                'score': assignment.score,
                'completed_at': assignment.completed_at,
                'blockchain_verified': blockchain_record is not None
            }
            
            if blockchain_record:
                record['blockchain'] = {
                    'record_hash': blockchain_record.record_hash,
                    'tx_hash': blockchain_record.tx_hash,
                    'block_number': blockchain_record.block_number,
                    'verification_url': f"{settings.BLOCKCHAIN_EXPLORER_URL}/tx/{blockchain_record.tx_hash}"
                }
            
            history.append(record)
        
        return history
    
    async def generate_audit_report(
        self,
        department: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive audit report with blockchain verification
        """
        from models.training import TrainingAssignment
        from models.user import User
        from models.blockchain import BlockchainRecord
        
        # Build query
        query = db.query(TrainingAssignment).join(User)
        
        if department:
            query = query.filter(User.department == department)
        
        if start_date:
            query = query.filter(TrainingAssignment.completed_at >= start_date)
        
        if end_date:
            query = query.filter(TrainingAssignment.completed_at <= end_date)
        
        assignments = query.all()
        
        # Collect statistics
        total_records = len(assignments)
        verified_records = 0
        blockchain_records = []
        
        for assignment in assignments:
            blockchain_record = db.query(BlockchainRecord).filter(
                BlockchainRecord.training_assignment_id == assignment.id
            ).first()
            
            if blockchain_record:
                verified_records += 1
                blockchain_records.append({
                    'user': assignment.user.email,
                    'module': assignment.module.name,
                    'completed_at': assignment.completed_at,
                    'record_hash': blockchain_record.record_hash,
                    'tx_hash': blockchain_record.tx_hash
                })
        
        # Calculate verification rate
        verification_rate = (verified_records / total_records * 100) if total_records > 0 else 0
        
        # Generate Merkle root for all records
        merkle_root = self._generate_merkle_root([r['record_hash'] for r in blockchain_records])
        
        return {
            'report_id': hashlib.sha256(f"{department}{datetime.now()}".encode()).hexdigest()[:16],
            'generated_at': datetime.now().isoformat(),
            'filters': {
                'department': department,
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            },
            'statistics': {
                'total_training_records': total_records,
                'blockchain_verified': verified_records,
                'verification_rate': round(verification_rate, 2),
                'unverified_records': total_records - verified_records
            },
            'blockchain_summary': {
                'merkle_root': merkle_root,
                'total_transactions': len(blockchain_records),
                'earliest_block': min([r['tx_hash'] for r in blockchain_records]) if blockchain_records else None,
                'latest_block': max([r['tx_hash'] for r in blockchain_records]) if blockchain_records else None
            },
            'records': blockchain_records,
            'verification_status': 'VERIFIED' if verification_rate == 100 else 'PARTIAL' if verification_rate > 0 else 'UNVERIFIED'
        }
    
    def _generate_merkle_root(self, hashes: List[str]) -> str:
        """
        Generate Merkle root from list of hashes
        """
        if not hashes:
            return None
        
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            
            new_level = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i + 1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(new_hash)
            
            hashes = new_level
        
        return hashes[0]

class SmartContractManager:
    """
    Manage blockchain smart contracts for training audit
    """
    
    def __init__(self):
        self.contracts = {}
        
    def deploy_training_contract(self, network: str = 'development') -> Dict[str, Any]:
        """
        Deploy training audit smart contract
        """
        # This would compile and deploy the Solidity contract
        # For demo, return mock deployment info
        
        contract_address = Web3.keccak(text=f"TrainingAudit_{datetime.now()}").hex()[:40]
        
        return {
            'contract_name': 'TrainingAudit',
            'network': network,
            'address': f"0x{contract_address}",
            'deployed_at': datetime.now().isoformat(),
            'transaction_hash': f"0x{Web3.keccak(text='deploy_tx').hex()}"
        }
    
    def get_contract_events(self, contract_address: str, event_name: str, from_block: int = 0) -> List[Dict]:
        """
        Get events from smart contract
        """
        # This would query blockchain for events
        return []

# Solidity Smart Contract (TrainingAudit.sol)
"""
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TrainingAudit {
    
    struct TrainingRecord {
        string recordHash;
        string metadata;
        uint256 timestamp;
        address recordedBy;
    }
    
    mapping(string => TrainingRecord) private records;
    mapping(address => string[]) private userRecords;
    
    event RecordStored(string indexed recordHash, address indexed recordedBy, uint256 timestamp);
    event RecordVerified(string indexed recordHash, bool verified);
    
    function storeRecord(string memory recordHash, string memory metadata) public {
        require(bytes(recordHash).length > 0, "Record hash cannot be empty");
        require(bytes(records[recordHash].recordHash).length == 0, "Record already exists");
        
        records[recordHash] = TrainingRecord({
            recordHash: recordHash,
            metadata: metadata,
            timestamp: block.timestamp,
            recordedBy: msg.sender
        });
        
        userRecords[msg.sender].push(recordHash);
        
        emit RecordStored(recordHash, msg.sender, block.timestamp);
    }
    
    function getRecord(string memory recordHash) public view returns (string memory) {
        require(bytes(records[recordHash].recordHash).length > 0, "Record not found");
        return records[recordHash].metadata;
    }
    
    function verifyRecord(string memory recordHash) public view returns (bool) {
        return bytes(records[recordHash].recordHash).length > 0;
    }
    
    function getUserRecords(address user) public view returns (string[] memory) {
        return userRecords[user];
    }
    
    function getRecordTimestamp(string memory recordHash) public view returns (uint256) {
        require(bytes(records[recordHash].recordHash).length > 0, "Record not found");
        return records[recordHash].timestamp;
    }
}
"""

# Initialize blockchain service
blockchain_service = BlockchainAuditService()
