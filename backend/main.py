from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analyzer import analyze_job
from job_scraper import scrape_job_url
from database import save_analysis, get_analysis_history


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="JobShield AI",
    description="AI-powered Fake Job & Internship Detection System",
    version="1.0.0"
)


# ==========================================
# CORS Configuration
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Request Models
# ==========================================

class JobRequest(BaseModel):
    job_text: str


class URLRequest(BaseModel):
    url: str


# ==========================================
# Home Endpoint
# ==========================================

@app.get("/")
def home():

    return {
        "message": "JobShield AI API is running",
        "status": "success"
    }


# ==========================================
# Analyze Job Text
# ==========================================

@app.post("/analyze")
def analyze(request: JobRequest):

    # Analyze the job
    result = analyze_job(request.job_text)

    # Get company name
    company_name = result[
        "company_verification"
    ].get("company_name")

    # Save analysis to PostgreSQL
    save_analysis(
        job_text=request.job_text,
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        company_name=company_name,
        recommendation=result["recommendation"]
    )

    return {
        "job_text": request.job_text,
        "analysis": result
    }


# ==========================================
# Analyze Job URL
# ==========================================

@app.post("/analyze-url")
def analyze_url(request: URLRequest):

    # Scrape the webpage
    scraped = scrape_job_url(
        request.url
    )

    # Handle scraping failure
    if not scraped["success"]:

        return {
            "success": False,
            "error": scraped["error"]
        }

    # Analyze scraped job text
    analysis = analyze_job(
        scraped["text"]
    )

    # Get company name
    company_name = analysis[
        "company_verification"
    ].get("company_name")

    # Save analysis to PostgreSQL
    save_analysis(
        job_text=scraped["text"],
        risk_score=analysis["risk_score"],
        risk_level=analysis["risk_level"],
        company_name=company_name,
        recommendation=analysis["recommendation"]
    )

    return {
        "success": True,
        "url": request.url,
        "title": scraped["title"],
        "analysis": analysis
    }


# ==========================================
# Analysis History
# ==========================================

@app.get("/history")
def history():

    rows = get_analysis_history()

    results = []

    for row in rows:

        results.append({
            "id": row[0],
            "job_text": row[1],
            "risk_score": row[2],
            "risk_level": row[3],
            "company_name": row[4],
            "recommendation": row[5],
            "created_at": row[6]
        })

    return {
        "count": len(results),
        "history": results
    }