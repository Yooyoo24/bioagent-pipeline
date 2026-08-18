from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import BioAgentPipeline

app = FastAPI(
    title="BioAgent-Pipeline Service",
    description="Production-grade AI agent service for biomedical data aggregation and analysis.",
    version="1.0.0"
)

pipeline = BioAgentPipeline()

class AnalysisRequest(BaseModel):
    query: str
    require_human_approval: bool = True

class AnalysisResponse(BaseModel):
    status: str
    query: str
    report: str

@app.get("/")
def health_check():
    return {"status": "online", "service": "BioAgent-Pipeline"}

@app.post("/api/v1/analyze", response_model=AnalysisResponse)
def analyze_biological_target(request: AnalysisRequest):
    try:
        result = pipeline.run_pipeline(request.query, request.require_human_approval)
        return AnalysisResponse(
            status="success",
            query=request.query,
            report=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))