from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as routes_router
from integrations import router as integrations_router
from vishing import router as vishing_router
from blockchain import router as blockchain_router
from gamification import router as gamification_router
from mobile import router as mobile_router
from auth import router as auth_router

app = FastAPI(
    title="Phishing Simulation Platform API",
    description="Backend API for the Phishing Simulation Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "http://192.168.100.129:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers - FIXED: removed duplicate /auth prefix since auth.py already has it
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(routes_router, prefix="/api", tags=["Routes"])
app.include_router(integrations_router, prefix="/api", tags=["Integrations"])
app.include_router(vishing_router, prefix="/api", tags=["Vishing"])
app.include_router(blockchain_router, prefix="/api", tags=["Blockchain"])
app.include_router(gamification_router, prefix="/api", tags=["Gamification"])
app.include_router(mobile_router, prefix="/api", tags=["Mobile"])

@app.get("/")
async def root():
    return {
        "message": "Phishing Simulation Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "status": "ok",
        "message": "API is working",
        "endpoints": {
            "auth": "/api/auth/demo-login",
            "vishing": "/api/vishing/calls/active",
            "blockchain": "/api/blockchain/certificates",
            "mobile": "/api/mobile/devices",
            "integrations": "/api/integrations/webhooks",
            "gamification": "/api/gamification/leaderboard"
        }
    }

@app.get("/api/debug/routes")
async def debug_routes():
    """List all registered routes for debugging"""
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    return {"routes": routes}
