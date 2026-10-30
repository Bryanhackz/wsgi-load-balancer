import http.client
import urllib.parse
import threading
from db import get_healthy_backends

_lock = threading.Lock()
_current_index = 0

ALLOWED_HEADERS = {
    "HTTP_ACCEPT", "HTTP_ACCEPT_ENCODING", "HTTP_ACCEPT_LANGUAGE",
    "HTTP_USER_AGENT", "HTTP_AUTHORIZATION", "CONTENT_TYPE", "CONTENT_LENGTH"
}

def get_next_backend() -> str | None:
    global _current_index
    backends = get_healthy_backends()
    if not backends:
        return None
        
    with _lock:
        backend = backends[_current_index % len(backends)]
        _current_index += 1
        return backend

def forward_request(environ: dict, backend_url: str) -> tuple[str, list[tuple[str, str]], bytes]:
    parsed_url = urllib.parse.urlparse(backend_url)
    host = parsed_url.hostname
    port = parsed_url.port or 80
    
    conn = http.client.HTTPConnection(host, port, timeout=5)
    
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    query = environ.get("QUERY_STRING", "")
    if query:
        path += f"?{query}"

    body = b""
    try:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
        if content_length > 0:
            body = environ["wsgi.input"].read(content_length)
    except ValueError:
        pass

    headers = {}
    for key, value in environ.items():
        if key in ALLOWED_HEADERS:
            header_name = key[5:].replace("_", "-") if key.startswith("HTTP_") else key.replace("_", "-")
            headers[header_name] = value

    try:
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        resp_body = response.read()
        
        resp_headers = []
        for k, v in response.getheaders():
            if k.lower() not in ("connection", "transfer-encoding", "content-length"):
                resp_headers.append((k, v))
                
        return f"{response.status} {response.reason}", resp_headers, resp_body
    except Exception as e:
        return "502 Bad Gateway", [("Content-Type", "text/plain")], f"Proxy Error: {str(e)}".encode("utf-8")
    finally:
        conn.close()
