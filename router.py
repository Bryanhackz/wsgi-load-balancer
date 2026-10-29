from security.headers import get_security_headers
from handlers import pages, static, api
from balancer import get_next_backend, forward_request

def application(environ: dict, start_response: callable) -> list[bytes]:
    path = environ.get("PATH_INFO", "/")
    
    # Internal endpoints for the Dashboard (not proxied)
    if path.startswith("/api/"):
        status, content_type, body = api.handle_api(path)
        headers = [("Content-Type", content_type)]
    elif path in ("/", "/style.css", "/main.js", "/favicon.ico"):
        if path == "/":
            status, content_type, body = pages.render_index()
        else:
            static_result = static.serve_static(path)
            status, content_type, body = static_result if static_result else ("404 Not Found", "text/plain", "Not Found")
        headers = [("Content-Type", content_type)]
    else:
        # Proxy logic for everything else
        backend = get_next_backend()
        if not backend:
            status = "503 Service Unavailable"
            content_type = "text/plain"
            body = "No healthy backends available."
            headers = [("Content-Type", content_type)]
        else:
            status, proxy_headers, body = forward_request(environ, backend)
            headers = proxy_headers
            # Inject our security headers instead of the backend's
            headers = [(k, v) for k, v in headers if k.lower() not in ("content-security-policy", "x-frame-options")]

    for h, v in get_security_headers().items():
        headers.append((h, v))

    body_bytes = body.encode("utf-8") if isinstance(body, str) else body
    start_response(status, headers)
    return [body_bytes]