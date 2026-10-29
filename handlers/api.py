import json
from db import get_connection

def handle_api(path: str) -> tuple[str, str, str]:
    if path == "/api/status":
        with get_connection() as conn:
            rows = conn.execute("SELECT url, is_healthy, last_checked FROM backends").fetchall()
            data = [dict(row) for row in rows]
        return "200 OK", "application/json", json.dumps({"backends": data})
    
    return "404 Not Found", "application/json", json.dumps({"error": "Not found"})