// Função para alternar entre formulários
function trocarForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    loginForm.classList.toggle('active');
    registerForm.classList.toggle('active');
}

document.getElementById('enviar-login').addEventListener('click', async (e) => {
    e.preventDefault(); // Impede o comportamento padrão do formulário, por exemplo, recarregar a página
    
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-senha').value;
    
    try {
        const response = await fetch('http://localhost:5000/login', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                email: email,
                senha: senha 
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            // Armazena o token/localStorage para futuras requisições
            localStorage.setItem('token', data.token || '');

            localStorage.setItem('usuario', JSON.stringify(data.usuario));
            
            // Redireciona para a página do jogo
            window.location.href = '../jogo/jogo.html'; 
        } else {
            alert(data.message || 'Email ou senha incorretos');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor: ' + error.message);
    }
});


// Função de registro
document.getElementById('enviar-registro').addEventListener('click', async () => {
    const nome = document.getElementById('reg-nome').value;  
    const email = document.getElementById('reg-email').value;
    const senha = document.getElementById('reg-senha').value;
    
    try {
        const response = await fetch('http://localhost:5000/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome, email, senha }) 
        });

        const data = await response.json();
        if (response.ok) {
            alert('Cadastro realizado com sucesso!');
            trocarForms();  // Volta para o login
        } else {
            alert(data.message || 'Erro no cadastro');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor: ' + error.message);
    }
});