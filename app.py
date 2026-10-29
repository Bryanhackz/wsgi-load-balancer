import threading
from wsgiref.simple_server import make_server
from router import application
from db import init_db
from health import check_backends_loop

def main():
    init_db()
    
    # Start background health checker
    stop_event = threading.Event()
    health_thread = threading.Thread(target=check_backends_loop, args=(stop_event,), daemon=True)
    health_thread.start()
    
    port = 8080
    print(f"Load Balancer running on http://localhost:{port}")
    print("Health checker running in background.")
    
    with make_server("", port, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            stop_event.set()

if __name__ == "__main__":
    main()