from fastapi import APIRouter
from app.schemas.coverage import CoverageRequest

router = APIRouter()

@router.post("/coverage/run")
def run_coverage(req: CoverageRequest):
    return {"job_id": "mock-123", "status": "queued"}
