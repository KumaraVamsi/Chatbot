// Empty frontend script.js file
async function sendMessage() {
    const inputBox = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    const userText = inputBox.value.trim();
    if (!userText) return;

    // Display user message
    const userMessageEl = document.createElement('div');
    userMessageEl.className = 'message user-message';
    userMessageEl.innerText = userText;
    chatBox.appendChild(userMessageEl);

    inputBox.value = '';

    // Send API request to Flask backend
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: userText })
        });
        const data = await res.json();

        const botMessageEl = document.createElement('div');
        botMessageEl.className = 'message bot-message';
        botMessageEl.innerText = data.response;
        chatBox.appendChild(botMessageEl);

        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        console.error(err);
    }
}
