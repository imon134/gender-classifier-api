import httpx
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
import urllib.parse

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        name = params.get("name", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if not name or name.strip() == "":
            self.wfile.write(bytes(
                '{"status":"error","message":"Name query parameter is required"}',
                "utf8"
            ))
            return

        try:
            r = httpx.get("https://api.genderize.io", params={"name": name})
            data = r.json()

            gender = data.get("gender")
            probability = data.get("probability")
            count = data.get("count")

            if gender is None or count == 0:
                self.wfile.write(bytes(
                    '{"status":"error","message":"No prediction available for the provided name"}',
                    "utf8"
                ))
                return

            is_confident = probability >= 0.7 and count >= 100

            response = {
                "status": "success",
                "data": {
                    "name": name,
                    "gender": gender,
                    "probability": probability,
                    "sample_size": count,
                    "is_confident": is_confident,
                    "processed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                }
            }

            import json
            self.wfile.write(bytes(json.dumps(response), "utf8"))

        except Exception:
            self.wfile.write(bytes(
                '{"status":"error","message":"External API failure"}',
                "utf8"
            ))