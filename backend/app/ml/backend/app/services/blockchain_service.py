class BlockchainService:
    def __init__(self):
        pass
    
    async def get_status(self):
        return {"status": "connected"}

blockchain_service = BlockchainService()
