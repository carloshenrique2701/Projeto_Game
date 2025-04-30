// Função para alternar entre formulários
function trocarForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    loginForm.classList.toggle('active');
    registerForm.classList.toggle('active');
}

// Login tradicional
document.getElementById('enviar-login').addEventListener('click', async () => {
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-senha').value;
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({ email, senha })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Redireciona para a página do jogo após login
            window.location.href = '/jogo/jogo.html';
        } else {
            showAlert(data.error || 'Erro no login', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showAlert('Erro ao conectar com o servidor', 'error');
    }
});

// Login com Google
document.getElementById('google-login').addEventListener('click', () => {
    window.location.href = '/auth/google';
});

// Registro tradicional
document.getElementById('enviar-registro').addEventListener('click', async () => {
    const userData = {
        nome: document.getElementById('reg-nome').value,
        email: document.getElementById('reg-email').value,
        senha: document.getElementById('reg-senha').value,
        dataNasc: document.getElementById('reg-data').value
    };
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Registro realizado com sucesso!', 'success');
            toggleForms();
            // Limpa o formulário
            document.getElementById('register-form').reset();
        } else {
            showAlert(data.error || 'Erro no registro', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showAlert('Erro ao conectar com o servidor', 'error');
    }
});

// Função para exibir alertas
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    document.body.prepend(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}