function showApelidoModal() {
    document.querySelector('.apelido').style.display = 'flex';
    document.body.classList.add('modal-open-apelido');
    
    // Foca no input automaticamente para facilitar a digitação
    document.querySelector('.apelido input').focus();
}

function closeAllModals() {
    // Fecha todos os modais (incluindo o de apelido)
    const modals = document.querySelectorAll('.modal, .apelido');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
    
    // Remove o overlay
    const overlay = document.querySelector('.modal-overlay');
    if (overlay) overlay.style.display = 'none';
    
    // Remove a classe do body
    document.body.classList.remove('modal-open-apelido');
}


document.addEventListener('DOMContentLoaded', async () => {
    // Verifica se usuário está logado
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    if (!usuario || !usuario.id) {
        window.location.href = '../../public/index.html';
        return;
    }

    // Verifica se já tem apelido
    await verificarApelido(usuario.id);
});

async function verificarApelido(usuarioId) {
    try {
        const response = await fetch(`http://localhost:5000/check-apelido?usuario_id=${usuarioId}`);
        const data = await response.json();
        
        if (!data.temApelido) {
            // Mostra modal para cadastrar apelido
            showApelidoModal();
        } else {
            // Atualiza o apelido na interface
            document.getElementById('apelido').textContent = data.apelido;
        }
    } catch (error) {
        console.error('Erro ao verificar apelido:', error);
        alert('Erro ao verificar apelido. Por favor, recarregue a página.');
    }
}

async function registrarApelido() {
    const apelidoInput = document.querySelector('.apelido input');
    const apelido = apelidoInput.value.trim();
    const feedbackElement = document.getElementById('apelido-feedback');
    
    feedbackElement.style.display = 'none';
    
    if (!apelido) {
        feedbackElement.textContent = 'Por favor, digite um apelido';
        feedbackElement.style.display = 'block';
        return;
    }
    
    try {
        const usuario = JSON.parse(localStorage.getItem('usuario'));
        console.log('Tentando registrar apelido:', apelido);
        
        const response = await fetch('http://localhost:5000/registrar-apelido', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                usuario_id: usuario.id,
                apelido: apelido
            })
        });
        
        const data = await response.json();
        console.log('Resposta do registro:', data);
        
        if (!response.ok || !data.success) {
            throw new Error(data.message || 'Erro ao registrar apelido');
        }
        closeAllModals();
        
        // Atualiza a interface
        document.querySelector('.apelido').style.display = 'none';
        document.getElementById('apelido').textContent = apelido;
        
        // Atualiza o usuário no localStorage
        usuario.apelido = apelido;
        localStorage.setItem('usuario', JSON.stringify(usuario));
        
    } catch (error) {
        console.error('Erro no registro:', error);
        feedbackElement.textContent = error.message;
        feedbackElement.style.display = 'block';
        apelidoInput.focus();
    }
}