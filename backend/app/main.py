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
from backend.app.routes.dataset import router as dataset_router

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
app.include_router(dataset_router)

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Locate frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")

if os.path.exists(FRONTEND_DIR):
    css_dir = os.path.join(FRONTEND_DIR, "css")
    js_dir = os.path.join(FRONTEND_DIR, "js")
    assets_dir = os.path.join(FRONTEND_DIR, "assets")
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/styles.css", include_in_schema=False)
def serve_styles():
    styles_file = os.path.join(FRONTEND_DIR, "styles.css")
    if os.path.exists(styles_file):
        return FileResponse(styles_file, media_type="text/css")

@app.get("/app.js", include_in_schema=False)
def serve_app_js():
    js_file = os.path.join(FRONTEND_DIR, "app.js")
    if os.path.exists(js_file):
        return FileResponse(js_file, media_type="application/javascript")

@app.get("/", tags=["UI"])
def root():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "service": APP_NAME,
        "version": VERSION,
        "docs_url": "/docs",
        "author": "Saksham (Backend Engineer)"
    }

@app.get("/health", tags=["Health"])
def health():
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
