from pathlib import Path
import mimetypes
from urllib.parse import unquote

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

def serve_static(path: str) -> tuple[str, str, bytes] | None:
    safe_path = unquote(path).lstrip("/")
    full_path = (FRONTEND_DIR / safe_path).resolve()

    if not str(full_path).startswith(str(FRONTEND_DIR)):
        return None

    if full_path.is_file():
        mime_type, _ = mimetypes.guess_type(full_path)
        mime_type = mime_type or "application/octet-stream"

        if mime_type.startswith("text/") or mime_type in ("application/javascript", "application/json"):
            mime_type += "; charset=utf-8"

        return "200 OK", mime_type, full_path.read_bytes()

    return None