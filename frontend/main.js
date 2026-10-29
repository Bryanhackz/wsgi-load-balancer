async function updateStatus() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        const container = document.getElementById('backend-list');
        
        container.innerHTML = data.backends.map(b => `
            <div class="card">
                <span>${b.url}</span>
                <span class="${b.is_healthy ? 'status-ok' : 'status-dead'}">
                    ${b.is_healthy ? 'ONLINE' : 'OFFLINE'}
                </span>
            </div>
        `).join('');
    } catch (e) {
        console.error("Failed to fetch status");
    }
}

setInterval(updateStatus, 2000);
updateStatus();