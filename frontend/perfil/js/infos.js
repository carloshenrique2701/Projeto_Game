document.addEventListener('DOMContentLoaded', async () => {
    // Verifica se usuário está logado
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    if (!usuario || !usuario.id) {
        window.location.href = '../../public/index.html';
        return;
    }

    // Carrega as informações do perfil
    await carregarPerfil(usuario.id);
});

async function carregarPerfil(usuarioId) {
    try {
        const response = await fetch(`http://localhost:5000/perfil-usuario?usuario_id=${usuarioId}`);
        
        if (!response.ok) {
            throw new Error('Erro ao carregar perfil');
        }
        
        const data = await response.json();
        
        // Atualiza a interface
        document.getElementById('apelido').textContent = data.apelido || 'Sem apelido';
        document.getElementById('nome').textContent = data.nome;
        document.getElementById('email').textContent = data.email;
        
    } catch (error) {
        console.error('Erro ao carregar perfil:', error);
        alert('Erro ao carregar informações do perfil. Por favor, recarregue a página.');
    }
}

function alterarApelido() {
    const novoApelido = document.getElementById('alterApelido').value.trim();
    const feedbackElement = document.createElement('div');
    feedbackElement.className = 'feedback-message';
    
    if (!novoApelido) {
        showFeedback('Por favor, digite um apelido válido', 'error');
        return;
    }
    
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    
    fetch('http://localhost:5000/alterar-apelido', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            usuario_id: usuario.id,
            novo_apelido: novoApelido
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showFeedback('Apelido atualizado com sucesso!', 'success');
            document.getElementById('apelido').textContent = data.novo_apelido;
            closeAllModals();
            
            // Atualiza o localStorage
            usuario.apelido = data.novo_apelido;
            localStorage.setItem('usuario', JSON.stringify(usuario));
        } else {
            showFeedback(data.message || 'Erro ao atualizar apelido', 'error');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showFeedback('Erro ao conectar com o servidor', 'error');
    });
}

function showFeedback(message, type) {
    const feedbackElement = document.createElement('div');
    feedbackElement.className = `feedback-message ${type}`;
    feedbackElement.textContent = message;
    
    const container = document.querySelector('.content');
    container.insertBefore(feedbackElement, container.firstChild);
    
    setTimeout(() => {
        feedbackElement.remove();
    }, 5000);
}