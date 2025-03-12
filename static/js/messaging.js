document.addEventListener('DOMContentLoaded', function() {
    // 发送新消息
    const newMessageForm = document.getElementById('newMessageForm');
    if (newMessageForm) {
        newMessageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = {
                receiver: document.getElementById('receiver').value,
                subject: document.getElementById('subject').value,
                content: document.getElementById('content').value
            };

            fetch('/api/messages/send_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    $('#newMessageModal').modal('hide');
                    location.reload();
                }
            });
        });
    }

    // 聊天功能
    const messageForm = document.getElementById('messageForm');
    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const content = document.getElementById('messageInput').value;
            const chatUserId = window.location.pathname.split('/').slice(-2)[0];

            fetch('/api/messages/send_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    receiver: chatUserId,
                    content: content
                })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    document.getElementById('messageInput').value = '';
                    appendMessage(data);
                }
            });
        });
    }
});

function appendMessage(message) {
    const container = document.getElementById('messageContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message sent`;
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${message.content}</p>
            <small class="text-muted">${new Date().toLocaleString()}</small>
        </div>
    `;
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}