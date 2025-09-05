// Global variables
let currentConversationId = null;
let conversations = [];
let isLoading = false;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    loadConversations();
    updateSendButtonState();
    
    // Add input event listener for textarea
    const messageInput = document.getElementById('messageInput');
    messageInput.addEventListener('input', function() {
        updateSendButtonState();
        adjustTextareaHeight(this);
    });
});

// Load conversations from the server
async function loadConversations() {
    try {
        const response = await fetch('/api/conversations');
        conversations = await response.json();
        renderConversations();
    } catch (error) {
        console.error('Error loading conversations:', error);
    }
}

// Render conversations in the sidebar
function renderConversations() {
    const conversationsList = document.getElementById('conversationsList');
    
    if (conversations.length === 0) {
        conversationsList.innerHTML = '<div class="no-conversations">No conversations yet</div>';
        return;
    }
    
    conversationsList.innerHTML = conversations.map(conv => `
        <div class="conversation-item ${conv.id === currentConversationId ? 'active' : ''}" 
             onclick="selectConversation(${conv.id})">
            <div class="conversation-title">${conv.title}</div>
            <div class="conversation-actions">
                <button class="action-btn" onclick="deleteConversation(${conv.id}, event)">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Create a new conversation
async function createNewChat() {
    try {
        const response = await fetch('/api/conversations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const newConversation = await response.json();
        conversations.unshift(newConversation);
        selectConversation(newConversation.id);
        renderConversations();
    } catch (error) {
        console.error('Error creating new chat:', error);
        alert('Failed to create new chat');
    }
}

// Select a conversation
async function selectConversation(conversationId) {
    currentConversationId = conversationId;
    renderConversations();
    await loadMessages(conversationId);
    hideWelcomeScreen();
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        closeSidebar();
    }
}

// Load messages for a conversation
async function loadMessages(conversationId) {
    try {
        const response = await fetch(`/api/conversations/${conversationId}/messages`);
        const messages = await response.json();
        renderMessages(messages);
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

// Render messages in the chat container
function renderMessages(messages) {
    const messagesContainer = document.getElementById('messagesContainer');
    
    messagesContainer.innerHTML = messages.map(msg => `
        <div class="message ${msg.role}-message">
            <div class="message-avatar ${msg.role}-avatar">
                ${msg.role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>'}
            </div>
            <div class="message-content">
                <div class="message-text">${formatMessage(msg.content)}</div>
            </div>
        </div>
    `).join('');
    
    scrollToBottom();
}

// Format message content (basic markdown support)
function formatMessage(content) {
    // Basic code block support
    content = content.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    // Inline code
    content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Line breaks
    content = content.replace(/\n/g, '<br>');
    
    return content;
}

// Send a message
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message || isLoading) return;
    
    // Create conversation if none selected
    if (!currentConversationId) {
        await createNewChat();
    }
    
    // Clear input and disable send button
    messageInput.value = '';
    adjustTextareaHeight(messageInput);
    updateSendButtonState();
    isLoading = true;
    
    // Add user message to UI immediately
    addMessageToUI('user', message);
    
    // Add typing indicator
    addTypingIndicator();
    
    try {
        const response = await fetch(`/api/conversations/${currentConversationId}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add AI response to UI
            addMessageToUI('assistant', data.ai_message.content);
            
            // Update conversation title if it changed
            await loadConversations();
        } else {
            removeTypingIndicator();
            addMessageToUI('assistant', `Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        removeTypingIndicator();
        addMessageToUI('assistant', 'Sorry, there was an error processing your request.');
    } finally {
        isLoading = false;
        updateSendButtonState();
    }
}

// Add message to UI
function addMessageToUI(role, content) {
    const messagesContainer = document.getElementById('messagesContainer');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    messageDiv.innerHTML = `
        <div class="message-avatar ${role}-avatar">
            ${role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>'}
        </div>
        <div class="message-content">
            <div class="message-text">${formatMessage(content)}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add typing indicator
function addTypingIndicator() {
    const messagesContainer = document.getElementById('messagesContainer');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant-message typing-message';
    typingDiv.innerHTML = `
        <div class="message-avatar assistant-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span>Thinking</span>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingMessage = document.querySelector('.typing-message');
    if (typingMessage) {
        typingMessage.remove();
    }
}

// Delete conversation
async function deleteConversation(conversationId, event) {
    event.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this conversation?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/conversations/${conversationId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            conversations = conversations.filter(conv => conv.id !== conversationId);
            
            if (currentConversationId === conversationId) {
                currentConversationId = null;
                showWelcomeScreen();
            }
            
            renderConversations();
        } else {
            alert('Failed to delete conversation');
        }
    } catch (error) {
        console.error('Error deleting conversation:', error);
        alert('Failed to delete conversation');
    }
}

// Handle keyboard shortcuts
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Adjust textarea height
function adjustTextareaHeight(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

// Update send button state
function updateSendButtonState() {
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    
    const hasText = messageInput.value.trim().length > 0;
    sendBtn.disabled = !hasText || isLoading;
}

// Set prompt from example cards
function setPrompt(prompt) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = prompt;
    adjustTextareaHeight(messageInput);
    updateSendButtonState();
    messageInput.focus();
}

// Show/hide welcome screen
function showWelcomeScreen() {
    document.getElementById('welcomeScreen').style.display = 'flex';
    document.getElementById('messagesContainer').innerHTML = '';
}

function hideWelcomeScreen() {
    document.getElementById('welcomeScreen').style.display = 'none';
}

// Scroll to bottom of messages
function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Sidebar toggle for mobile
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.remove('open');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    if (window.innerWidth <= 768 && 
        !sidebar.contains(event.target) && 
        !sidebarToggle.contains(event.target) &&
        sidebar.classList.contains('open')) {
        closeSidebar();
    }
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.remove('open');
    }
});
