document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message');

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value;
        socket.emit('message', { message });
        messageInput.value = '';
    });

    socket.on('message', (data) => {
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `<span style="color:${data.color}; font-weight:bold;">${data.username}</span>: ${data.message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    });
});
