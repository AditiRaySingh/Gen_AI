from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.analytics_service import process_query
from app.models.response_models import QueryResponse
from app.services.feedback import save_feedback


app = FastAPI(
    title="Intelligent Analytics Query Engine",
    description="Natural Language Analytics Engine using GenAI",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REQUEST MODELS
# =========================

class QueryRequest(BaseModel):
    query: str


class FeedbackRequest(BaseModel):
    query: str
    feedback: str


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "Intelligent Analytics Query Engine is running"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "analytics-query-engine"
    }


# =========================
# QUERY
# =========================

@app.post(
    "/api/query",
    response_model=QueryResponse
)
def run_query(request: QueryRequest):

    # Check empty query
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:

        result = process_query(
            request.query.strip()
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        print("Query processing error:", error)

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process the query. "
                "Please try rephrasing your question."
            )
        )


# =========================
# FEEDBACK
# =========================

@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    if request.feedback not in ["positive", "negative"]:
        raise HTTPException(
            status_code=400,
            detail="Feedback must be positive or negative."
        )

    try:

        return save_feedback(
            request.query.strip(),
            request.feedback
        )

    except Exception as error:

        print("Feedback error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to save feedback."
        )