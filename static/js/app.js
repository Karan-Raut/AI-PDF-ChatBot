document.addEventListener('DOMContentLoaded', () => {
    const pdfUpload = document.getElementById('pdf-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const uploadSubmitBtn = document.getElementById('upload-submit');
    const uploadStatus = document.getElementById('upload-status');
    const questionInput = document.getElementById('question-input');
    const sendBtn = document.getElementById('send-btn');
    const chatWindow = document.getElementById('chat-window');

    let isPdfUploaded = false;

    // File selection
    pdfUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            if (file.type !== 'application/pdf') {
                showStatus('Please select a valid PDF file.', 'error');
                fileNameDisplay.textContent = 'Invalid file type';
                uploadSubmitBtn.disabled = true;
                return;
            }
            fileNameDisplay.textContent = file.name;
            uploadSubmitBtn.disabled = false;
            hideStatus();
        } else {
            fileNameDisplay.textContent = 'No file chosen';
            uploadSubmitBtn.disabled = true;
        }
    });

    // Upload Action
    uploadSubmitBtn.addEventListener('click', async () => {
        const file = pdfUpload.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        uploadSubmitBtn.disabled = true;
        uploadSubmitBtn.innerHTML = 'Uploading...';
        showStatus('Uploading and parsing document, please wait...', '');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showStatus(`Success! Processed ${data.chunks} chunks.`, 'success');
                isPdfUploaded = true;
                questionInput.disabled = false;
                sendBtn.disabled = false;
                questionInput.focus();
            } else {
                showStatus(data.detail || 'Failed to upload PDF.', 'error');
            }
        } catch (error) {
            showStatus('Network error during upload.', 'error');
        } finally {
            uploadSubmitBtn.innerHTML = 'Upload & Process';
            uploadSubmitBtn.disabled = false;
        }
    });

    // Chat Send Action
    const sendMessage = async () => {
        if (!isPdfUploaded) {
            alert("Please upload a PDF first.");
            return;
        }
        
        const question = questionInput.value.trim();
        if (!question) return;

        // Add User Message
        appendMessage(question, 'user');
        questionInput.value = '';
        
        // Add Loading Indicator
        const loadingId = appendLoading();
        
        // Disable input while generating
        questionInput.disabled = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });

            const data = await response.json();
            removeElement(loadingId);

            if (response.ok) {
                appendMessage(data.answer, 'ai');
            } else {
                appendMessage(`Error: ${data.detail || 'Something went wrong.'}`, 'ai');
            }
        } catch (error) {
            removeElement(loadingId);
            appendMessage('Network error while asking question.', 'ai');
        } finally {
            questionInput.disabled = false;
            sendBtn.disabled = false;
            questionInput.focus();
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Helpers
    function showStatus(msg, type) {
        uploadStatus.textContent = msg;
        uploadStatus.className = `status-msg ${type}`;
    }

    function hideStatus() {
        uploadStatus.className = 'status-msg hidden';
    }

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-content';
        
        // Basic escaping
        const escapedText = document.createTextNode(text);
        
        // If it's an AI message, we could parse markdown here, but let's stick to text formatting
        contentDiv.style.whiteSpace = 'pre-wrap';
        contentDiv.appendChild(escapedText);
        
        msgDiv.appendChild(contentDiv);
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ai';
        msgDiv.id = id;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-content';
        
        contentDiv.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        
        msgDiv.appendChild(contentDiv);
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});
