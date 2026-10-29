import threading
import time
import urllib.request
import urllib.error
from db import get_connection, update_health

def check_backends_loop(stop_event: threading.Event):
    while not stop_event.is_set():
        with get_connection() as conn:
            backends = conn.execute("SELECT url FROM backends").fetchall()
            
        for row in backends:
            url = row["url"]
            try:
                req = urllib.request.Request(f"{url}/", method="HEAD")
                with urllib.request.urlopen(req, timeout=2):
                    update_health(url, True)
            except Exception:
                update_health(url, False)
                
        stop_event.wait(5) # Check every 5 seconds