from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import APP_NAME, VERSION, DESCRIPTION
from backend.app.database import engine, Base, SessionLocal
from backend.app.services.seed import seed_database_from_json

# Import all API routes
from backend.app.routes.dashboard import router as dashboard_router
from backend.app.routes.assets import router as assets_router
from backend.app.routes.risks import router as risks_router
from backend.app.routes.scenario import router as scenario_router
from backend.app.routes.optimize import router as optimize_router
from backend.app.routes.ai import router as ai_router
from backend.app.routes.compliance import router as compliance_router
from backend.app.routes.vulnerabilities import router as vulnerabilities_router

# Create Database tables on startup safely
try:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db_session:
        seed_database_from_json(db_session)
except Exception as e:
    print(f"[MAIN STARTUP NOTICE] Database initialization deferred: {e}")

# Initialize FastAPI App
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description=DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Mridul's Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(dashboard_router)
app.include_router(assets_router)
app.include_router(vulnerabilities_router)
app.include_router(risks_router)
app.include_router(scenario_router)
app.include_router(optimize_router)
app.include_router(ai_router)
app.include_router(compliance_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": APP_NAME,
        "version": VERSION,
        "docs_url": "/docs",
        "author": "Saksham (Backend Engineer)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
