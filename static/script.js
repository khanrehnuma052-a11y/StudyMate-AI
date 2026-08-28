const input = document.getElementById('study-input');
const result = document.getElementById('result');
const actionButtons = document.querySelectorAll('.action-button');

async function handleGenerate(action) {
    const topic = input.value.trim();
    if (!topic) {
        result.innerHTML = '<div class="error-message">Please enter a topic or paste some study notes first.</div>';
        input.focus();
        return;
    }

    actionButtons.forEach((button) => { button.disabled = true; });
    result.innerHTML = '<div class="loading"><div class="spinner" aria-hidden="true"></div><p>Thinking through your study material...</p></div>';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, action })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong. Please try again.');
        }
        result.innerHTML = `<div class="result-text">${escapeHtml(data.result)}</div>`;
    } catch (error) {
        result.innerHTML = `<div class="error-message">${escapeHtml(error.message || 'Network error. Please try again.')}</div>`;
    } finally {
        actionButtons.forEach((button) => { button.disabled = false; });
    }
}

function clearApp() {
    input.value = '';
    result.innerHTML = '<div class="empty-state"><div class="empty-icon" aria-hidden="true">✎</div><p>Your AI result will appear here.</p><span>Choose a study tool above to begin.</span></div>';
    input.focus();
}

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}
