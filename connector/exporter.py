import requests
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

# Configuration
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjgwNjM5MWUzLTBjMTYtNGNlNy05YzE5LWUxNTlhZjYwNmQyMSIsInR5cCI6ImtleSJ9.qTYU79rT3X22GUih9ljv5xGYQkhsEUN4tBppGhIgBis"
# Note: Inside Docker, we use the container name, not localhost
CHIRPSTACK_URL = "http://chirpstack-rest-api:8090/api"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

@app.get("/export/{resource}")
def export_data(resource: str):
    """Resource can be 'gateways' or 'devices'"""
    
    # 1. Fetch data from ChirpStack
    # We use ?limit=100 because the API defaults to 0 (empty list)
    url = f"{CHIRPSTACK_URL}/{resource}?limit=100"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="ChirpStack Error")

    data = response.json().get('result', [])
    
    # 2. Extract specific fields (Name, Lat, Lon, Alt)
    rows = []
    for item in data:
        loc = item.get('location', {})
        rows.append({
            "name": item.get('name'),
            "latitude": loc.get('latitude'),
            "longitude": loc.get('longitude'),
            "altitude": loc.get('altitude')
        })

    # 3. Convert to CSV using Pandas
    df = pd.DataFrame(rows)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    # 4. Return as a downloadable file
    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={resource}_export.csv"
    return response
