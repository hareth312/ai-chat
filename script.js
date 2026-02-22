const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// --- CONFIGURATION ---
// عند الرفع على استضافة، استبدل الرابط أدناه برابط الموقع الجديد
const API_URL = 'http://127.0.0.1:5000/chat';
// ----------------------

function appendMessage(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', role);
    msgDiv.innerHTML = `<div class="content">${content}</div>`;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage('user', text);
    userInput.value = '';

    // Show loading state (optional)
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'bot', 'loading');
    loadingDiv.innerText = 'جاري التفكير...';
    chatMessages.appendChild(loadingDiv);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        chatMessages.removeChild(loadingDiv);

        if (data.reply) {
            appendMessage('bot', data.reply);
        } else {
            appendMessage('bot', 'عذراً، حدث خطأ ما.');
        }
    } catch (error) {
        chatMessages.removeChild(loadingDiv);
        appendMessage('bot', 'يرجى التأكد من تشغيل ملف Python (app.py).');
        console.error('Error:', error);
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
