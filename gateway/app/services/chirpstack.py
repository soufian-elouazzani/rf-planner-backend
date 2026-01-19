import requests
import pandas as pd
import io


CHIRPSTACK_URL = "http://localhost:8090/api"
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjgwNjM5MWUzLTBjMTYtNGNlNy05YzE5LWUxNTlhZjYwNmQyMSIsInR5cCI6ImtleSJ9.qTYU79rT3X22GUih9ljv5xGYQkhsEUN4tBppGhIgBis"

def get_chirpstack_csv(resource: str):
    url = f"{CHIRPSTACK_URL}/gateways?limit=100&tenantId=83cb8472-10d3-44dd-a39b-95ea54582197"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    data = response.json().get('result', [])
    rows = []
    for item in data:
        loc = item.get('location', {})
        rows.append({
            "name": item.get('name'),
            "latitude": loc.get('latitude'),
            "longitude": loc.get('longitude')
        })

    df = pd.DataFrame(rows)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    return stream.getvalue()

