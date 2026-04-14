import httpx
from datetime import datetime, timezone

def handler(request):

    name = request.query_params.get("name")

    if not name or name.strip() == "":
        return {
            "status": "error",
            "message": "Name query parameter is required"
        }

    try:
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

    except Exception:
        return {
            "status": "error",
            "message": "External API failure"
        }