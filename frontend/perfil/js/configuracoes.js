

function openDiv(div) {
    // Criar overlay(sobreposição) se não existir
    let overlay = document.querySelector('.modal-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        document.body.appendChild(overlay);
        
        // Fechar modal ao clicar no overlay
        overlay.addEventListener('click', closeAllModals);
    }
    overlay.style.display = 'block';
    
    if(addEventListener('click', () => {
        
        console.log('click');

    }))
    // Fechar qualquer modal aberto
    closeAllModals();
    
    switch (div) {
        case 1:
            document.getElementById('alterSenha').classList.add('modal');
            document.getElementById('alterSenha').style.display = 'flex';
            break;
        case 2:
            document.getElementById('alterApelidoDiv').classList.add('modal');
            document.getElementById('alterApelidoDiv').style.display = 'flex';
            break;               
        case 3:
            document.getElementById('desativarContaDiv').classList.add('modal');
            document.getElementById('desativarContaDiv').style.display = 'flex';
            break;
        default:
            console.log("Não encontrado");
            overlay.style.display = 'none';
            break;
    }
}

function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
    
    const overlay = document.querySelector('.modal-overlay');
    if (overlay) overlay.style.display = 'none';
}



// Verificação do email
async function verificarEmail() {
    const emailInput = document.getElementById('verificacaoEmail');
    const email = emailInput.value.trim();
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    
    if (!email) {
        showFeedback('Por favor, digite seu email', 'error');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/verificar-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                usuario_id: usuario.id  // Verifica se o email pertence ao usuário
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Esconde a verificação e mostra o campo de nova senha
            document.querySelector('.verificacaoEmail').style.display = 'none';
            document.querySelector('.verificarSenha').style.display = 'flex';
            
            // Armazena o email validado no localStorage temporariamente
            localStorage.setItem('email_validado', email);
        } else {
            showFeedback(data.message || 'Email inválido', 'error');
            emailInput.focus();
        }
    } catch (error) {
        console.error('Erro:', error);
        showFeedback('Erro ao verificar email', 'error');
    }
}

// Alteração da senha
async function alterarSenha() {
    const novaSenhaInput = document.getElementById('verificarSenha');
    const novaSenha = novaSenhaInput.value.trim();
    const email = localStorage.getItem('email_validado');
    
    if (!novaSenha) {
        showFeedback('Por favor, digite uma nova senha', 'error');
        return;
    }

    if (novaSenha.length < 6) {
        showFeedback('Senha deve ter pelo menos 6 caracteres', 'error');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/alterar-senha', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                nova_senha: novaSenha
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showFeedback('Senha alterada com sucesso!', 'success');
            closeAllModals();
            
            // Limpa o email temporário
            localStorage.removeItem('email_validado');

        } else {
            showFeedback(data.message || 'Erro ao alterar senha', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showFeedback('Erro ao conectar com o servidor', 'error');
    }
}

// Função para mostrar feedback
function showFeedback(message, type) {
    // Remove feedbacks anteriores
    const feedbacks = document.querySelectorAll('.feedback-message');
    feedbacks.forEach(f => f.remove());
    
    // Cria novo feedback
    const feedbackElement = document.createElement('div');
    feedbackElement.className = `feedback-message ${type}`;
    feedbackElement.textContent = message;
    
    // Insere no modal de alteração de senha
    const modal = document.getElementById('alterSenha');
    modal.insertBefore(feedbackElement, modal.firstChild);
    
    // Remove após 5 segundos
    setTimeout(() => {
        feedbackElement.remove();
    }, 5000);
}


async function alterarApelido() {
    const novoApelidoInput = document.getElementById('alterApelido');
    const novoApelido = novoApelidoInput.value.trim();
    const usuario = JSON.parse(localStorage.getItem('usuario'));

    if (!novoApelido) {
        showFeedback('Por favor, digite um apelido', 'error');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/alterar-apelido-direto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                usuario_id: usuario.id,
                novo_apelido: novoApelido
            })
        });

        const data = await response.json();

        if (data.success) {
            showFeedback('Apelido alterado com sucesso!', 'success');
            
            // Atualiza a UI
            document.getElementById('apelido').textContent = data.novo_apelido;
            
            // Atualiza o localStorage
            usuario.apelido = data.novo_apelido;
            localStorage.setItem('usuario', JSON.stringify(usuario));
            
            // Fecha o modal
            closeAllModals();
        } else {
            showFeedback(data.message || 'Erro ao alterar apelido', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showFeedback('Erro ao conectar com o servidor', 'error');
    }
}



let senhaCorreta = false;

async function verificarSenhaDesativacao() {
    const senha = document.getElementById('senhaDesativacao').value.trim();
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    
    if (!senha) {
        showFeedback('Por favor, digite sua senha', 'error');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/verificar-senha', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                usuario_id: usuario.id,
                senha: senha
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            senhaCorreta = true;
            document.querySelector('.conf2').style.display = 'none';
            document.querySelector('.conf3').style.display = 'flex';
        } else {
            showFeedback('Senha incorreta', 'error');
            senhaCorreta = false;
        }
    } catch (error) {
        console.error('Erro:', error);
        showFeedback('Erro ao verificar senha', 'error');
    }
}

async function desativarConta() {
    if (!senhaCorreta) {
        showFeedback('Por favor, verifique sua senha primeiro', 'error');
        return;
    }

    const usuario = JSON.parse(localStorage.getItem('usuario'));
    
    try {
        const response = await fetch('http://localhost:5000/deletar-conta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                usuario_id: usuario.id
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Limpa o localStorage e redireciona
            localStorage.removeItem('usuario');
            window.location.href = '../public/index.html';
        } else {
            showFeedback(data.message || 'Erro ao deletar conta', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showFeedback('Erro ao conectar com o servidor', 'error');
    }
}


/**
 * Atualiza a preferência de tabela do usuário, informando se ele deseja
 * ser exibido na tabela de ranking ou não.
 */
async function atualizarPreferenciaTabela(mostrar) {
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    
    if (!usuario || !usuario.id) {
        console.error('Usuário não encontrado no localStorage');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/atualizar-preferencia-tabela', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                usuario_id: usuario.id,
                mostrar_na_tabela: mostrar
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('Preferência de tabela atualizada com sucesso');
        } else {
            console.error('Erro ao atualizar preferência de tabela');
        }
    } catch (error) {
        console.error('Erro ao conectar com o servidor:', error);
    }
}