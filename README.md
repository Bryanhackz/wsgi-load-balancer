# WSGI Load Balancer & Traffic Controller

## Problem
As web applications scale, a single server cannot handle the traffic load. A load balancer is required to distribute incoming requests across multiple backend servers, ensuring high availability and preventing any single point of failure.

## Solution
A zero-dependency, thread-safe WSGI Load Balancer written entirely in Python. It acts as a reverse proxy, distributing traffic using a Round Robin algorithm while continuously monitoring the health of its backend servers via background threads.

## Features
- **Reverse Proxy:** Forwards HTTP requests (including headers and body) transparently to backend servers.
- **Round Robin Distribution:** Distributes traffic sequentially across all healthy backends.
- **Automated Health Checks:** A background daemon thread pings the servers every 5 seconds. If a server dies, it is automatically removed from rotation. If it recovers, it is re-added.
- **Real-Time Dashboard:** A built-in Vanilla JS UI to monitor the status (ONLINE/OFFLINE) of all backends.
- **Zero Dependencies:** Built exclusively with the Python 3.11+ standard library (`wsgiref`, `http.client`, `sqlite3`, `threading`).

## Setup & Execution
Because this project demonstrates a distributed system, it requires multiple processes. Open four separate terminal windows in the project directory.

**1. Start the Backend Servers:**
```bash
# Terminal 1
python backend.py 8001

# Terminal 2
python backend.py 8002

# Terminal 3
python backend.py 8003
```

**2. Start the Load Balancer:**
```bash
# Terminal 4
python app.py
```
Open `http://localhost:8080` in your browser to view the dashboard.

## How to test it
1. Visit `http://localhost:8080/app`. Refresh the page several times. You will see the response alternate between ports `8001`, `8002`, and `8003`.
2. Kill one of the backend servers (Ctrl+C in one of the terminals).
3. Wait 5 seconds and refresh the dashboard (`http://localhost:8080`). The dead server will show as `OFFLINE`.
4. Keep hitting `/app`. The load balancer will seamlessly route traffic only to the remaining healthy servers.

## Architectural decisions
- **SQLite for State Management:** While a load balancer typically operates in memory, SQLite is used here to persist the health status of the backends. This ensures that if the load balancer itself restarts, it doesn't lose track of the infrastructure. WAL (Write-Ahead Logging) mode is enabled to allow concurrent reads from the API dashboard while the health checker writes updates.
- **Threading for Health Checks:** Health checks run in a separate daemon thread. This prevents the health check HTTP requests from blocking the main WSGI thread that is handling incoming client traffic.
- **Raw `http.client` for Proxying:** Instead of relying on heavy third-party libraries, the proxy logic uses the standard `http.client` module to reconstruct and forward the request to the upstream server, giving precise control over headers and timeouts.