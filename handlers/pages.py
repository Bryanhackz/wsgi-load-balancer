from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

def render_index() -> tuple[str, str, str]:
    html_path = FRONTEND_DIR / "index.html"
    try:
        html = html_path.read_text(encoding="utf-8")
        return "200 OK", "text/html; charset=utf-8", html
    except FileNotFoundError:
        return "500 Internal Server Error", "text/plain", "Template not found."

def not_found() -> tuple[str, str, str]:
    return "404 Not Found", "text/plain; charset=utf-8", "404 Not Found"