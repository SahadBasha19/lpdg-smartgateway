from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse,Response
from .database import init_db
from .routers import gateways,recommendations,analytics,admin
BASE=Path(__file__).resolve().parent.parent;FRONT=BASE/"frontend"
app=FastAPI(title="Smart Gateway Visit Recommendation Platform",version="2.0")
@app.on_event("startup")
def startup():init_db()
@app.get("/",include_in_schema=False)
def home():return FileResponse(FRONT/"index.html")
@app.get("/dashboard",include_in_schema=False)
def dashboard_page():return FileResponse(FRONT/"dashboard.html")
@app.get("/gateways",include_in_schema=False)
def gateways_page():return FileResponse(FRONT/"gateways.html")
@app.get("/risk",include_in_schema=False)
def risk_page():return FileResponse(FRONT/"risk.html")
@app.get("/analytics",include_in_schema=False)
def analytics_page():return FileResponse(FRONT/"analytics.html")
@app.get("/plots",include_in_schema=False)
def plots_page():return FileResponse(FRONT/"plots.html")
@app.get("/static.css",include_in_schema=False)
def css():return Response((FRONT/"style.css").read_text(),media_type="text/css")
@app.get("/app.js",include_in_schema=False)
def js():return Response((FRONT/"app.js").read_text(),media_type="application/javascript")
@app.get("/health")
def health():return {"status":"ok","service":"smart-gateway-api","version":"2.0"}
app.include_router(gateways.router);app.include_router(recommendations.router)
app.include_router(analytics.router);app.include_router(admin.router)
