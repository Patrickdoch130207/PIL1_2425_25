document.getElementById('userSearchInput').addEventListener('input', function() {
    const query = this.value;
    fetch(`/chat/conversations/users/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const usersList = document.getElementById('usersList');
            usersList.innerHTML = '';
            data.results.forEach(user => {
                usersList.innerHTML += `
                    <div class="user-item">
                        <span>${user.nom} ${user.prenom} (${user.email})</span>
                        <button class="btn btn-primary btn-sm start-chat-btn" data-email="${user.email}">Démarrer</button>
                    </div>
                `;
            });
        });
});
// Démarrer une conversation
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('start-chat-btn')) {
        const email = e.target.getAttribute('data-email');
        window.location.href = `/chat/conversations/${encodeURIComponent(email)}/`;
    }
});
// Affiche les conversations 
function displayConversations(conversations) {
    const conversationsList = document.getElementById('conversationsList');
    const emptyState = document.getElementById('emptyState');
    if (!conversations || conversations.length === 0) {
        conversationsList.innerHTML = '';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }
    if (emptyState) emptyState.style.display = 'none';
    conversationsList.innerHTML = conversations.map(conv => `
        <div>
            <a href="/chat/conversations/${encodeURIComponent(conv.email)}/">
                <b>${conv.name}</b> : ${conv.lastMessage}
            </a>
        </div>
    `).join('');
}

// Recherche dans les conversations
document.getElementById('searchInput').addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase();
    // conversations doit être défini côté JS ou passé depuis Django
    const filtered = conversations.filter(conv =>
        conv.name.toLowerCase().includes(query) ||
        conv.lastMessage.toLowerCase().includes(query)
    );
    displayConversations(filtered);
});


