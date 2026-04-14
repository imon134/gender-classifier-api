from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GENDERIZE_URL = "https://api.genderize.io"


@app.get("/")
async def classify(name: str = Query(None)):
    if name is None or name.strip() == "":
        return {"status": "error", "message": "Name query parameter is required"}

    async with httpx.AsyncClient() as client:
        r = await client.get(GENDERIZE_URL, params={"name": name})

    data = r.json()

    gender = data.get("gender")
    probability = data.get("probability")
    count = data.get("count")

    if gender is None or count == 0:
        return {
            "status": "error",
            "message": "No prediction available for the provided name"
        }

    sample_size = count
    is_confident = probability >= 0.7 and sample_size >= 100

    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
    }