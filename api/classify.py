import httpx
from datetime import datetime, timezone

def handler(request):

    name = request.args.get("name")

    if not name or name.strip() == "":
        return {
            "status": "error",
            "message": "Name query parameter is required"
        }

    r = httpx.get("https://api.genderize.io", params={"name": name})
    data = r.json()

    gender = data.get("gender")
    probability = data.get("probability")
    count = data.get("count")

    if gender is None or count == 0:
        return {
            "status": "error",
            "message": "No prediction available for the provided name"
        }

    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": count,
            "is_confident": probability >= 0.7 and count >= 100,
            "processed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
    }