from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.chirpstack import get_chirpstack_csv
import io

router = APIRouter()

@router.get("/csv/{resource}")
async def export_csv(resource: str):
    csv_data = get_chirpstack_csv(resource)
    if not csv_data:
        raise HTTPException(status_code=404, detail="Data not found")
        
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={resource}.csv"}
    )
