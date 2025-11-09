// Autodialer Frontend JavaScript

let logsPollingInterval = null;

// Show alert message
function showAlert(message, type = 'success') {
    const alertId = type === 'success' ? 'alert-success' : 'alert-error';
    const alertEl = document.getElementById(alertId);
    
    alertEl.textContent = message;
    alertEl.style.display = 'block';
    
    setTimeout(() => {
        alertEl.style.display = 'none';
    }, 5000);
}

// Upload phone numbers
async function uploadNumbers() {
    const fileInput = document.getElementById('file-upload');
    const pasteInput = document.getElementById('numbers-paste');
    
    const formData = new FormData();
    
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    } else if (pasteInput.value.trim()) {
        formData.append('numbers', pasteInput.value.trim());
    } else {
        showAlert('Please upload a file or paste numbers', 'error');
        return;
    }
    
    try {
        const response = await fetch('/upload-numbers', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(`Successfully loaded ${data.count} phone numbers`, 'success');
            
            // Show preview
            const previewBox = document.getElementById('numbers-preview');
            const previewContent = document.getElementById('preview-content');
            previewContent.textContent = data.numbers.join('\n') + 
                (data.count > 10 ? '\n... and more' : '');
            previewBox.style.display = 'block';
        } else {
            showAlert(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showAlert(`Upload failed: ${error.message}`, 'error');
    }
}

// Execute AI command
async function executeAICommand() {
    const commandInput = document.getElementById('ai-command');
    const command = commandInput.value.trim();
    
    if (!command) {
        showAlert('Please enter a command', 'error');
        return;
    }
    
    try {
        const response = await fetch('/ai-command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(
                `AI Command executed! Calling ${data.calls_initiated} number(s): ${data.parsed.numbers.join(', ')}`,
                'success'
            );
            commandInput.value = '';
            
            // Start polling logs
            startLogsPolling();
        } else {
            showAlert(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showAlert(`Command failed: ${error.message}`, 'error');
    }
}

// Start calling
async function startCalls() {
    const message = document.getElementById('call-message').value.trim();
    
    if (!message) {
        showAlert('Please enter a message', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('message', message);
    
    try {
        const response = await fetch('/start-calls', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(`Started calling ${data.calls_initiated} numbers`, 'success');
            
            // Start polling logs
            startLogsPolling();
        } else {
            showAlert(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showAlert(`Failed to start calls: ${error.message}`, 'error');
    }
}

// Stop calling (placeholder - in production would cancel pending calls)
function stopCalls() {
    stopLogsPolling();
    showAlert('Stopped calling (no new calls will be initiated)', 'success');
}

// Fetch and update logs
async function fetchLogs() {
    try {
        const response = await fetch('/logs');
        const data = await response.json();
        
        updateStats(data.stats);
        updateLogsTable(data.logs);
    } catch (error) {
        console.error('Failed to fetch logs:', error);
    }
}

// Update statistics
function updateStats(stats) {
    document.getElementById('stat-total').textContent = stats.total;
    document.getElementById('stat-progress').textContent = stats.in_progress;
    document.getElementById('stat-answered').textContent = stats.answered;
    document.getElementById('stat-failed').textContent = stats.failed;
}

// Update logs table
function updateLogsTable(logs) {
    const tbody = document.getElementById('logs-tbody');
    
    if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">No calls yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = logs.map(log => {
        const timestamp = new Date(log.timestamp).toLocaleString();
        const statusClass = getStatusClass(log.status);
        const displayStatus = log.error ? 'failed' : log.status;
        
        return `
            <tr>
                <td>${timestamp}</td>
                <td>${log.to_number}</td>
                <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" 
                    title="${escapeHtml(log.message)}">${escapeHtml(log.message)}</td>
                <td><span class="status ${statusClass}">${displayStatus}</span></td>
                <td style="font-family: monospace; font-size: 0.85em;">${log.call_sid || 'N/A'}</td>
            </tr>
        `;
    }).reverse().join('');  // Show newest first
}

// Get status CSS class
function getStatusClass(status) {
    if (status === 'failed' || status === 'busy' || status === 'no-answer') {
        return 'status-failed';
    } else if (status === 'in-progress' || status === 'ringing') {
        return 'status-progress';
    } else {
        return 'status-success';
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Start polling logs every 3 seconds
function startLogsPolling() {
    if (logsPollingInterval) {
        return; // Already polling
    }
    
    fetchLogs(); // Fetch immediately
    logsPollingInterval = setInterval(fetchLogs, 3000);
}

// Stop polling logs
function stopLogsPolling() {
    if (logsPollingInterval) {
        clearInterval(logsPollingInterval);
        logsPollingInterval = null;
    }
}

// Download logs as CSV
function downloadLogs() {
    window.location.href = '/logs/download';
}

// Initialize: fetch logs on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchLogs();
    
    // Auto-start polling if there are active calls
    // In production, you might check for active jobs
    
    // Allow Enter key to submit AI command
    document.getElementById('ai-command').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            executeAICommand();
        }
    });
});

