import sys
from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    port = environ.get("SERVER_PORT")
    body = f"Hello from Backend running on port {port}!".encode("utf-8")
    status = "200 OK"
    headers = [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))]
    start_response(status, headers)
    return [body]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backend.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    with make_server("", port, simple_app) as httpd:
        print(f"Backend running on port {port}")
        httpd.serve_forever()