// Função para mostrar/esconder as opções        
function showOptions(event) {
    // Impede que o evento se propague para o document
    event.stopPropagation();
    console.log('Abrindo opções');
    
    const divOptions = document.querySelector('.options');
    
    if (divOptions.style.display === 'block') {
        divOptions.style.display = 'none';
    } else {
        divOptions.style.display = 'block';
    }
}

// Função para esconder as opções ao clicar em qualquer parte da tela
function hideOptions(event) {
    console.log('Escondendo opções');
    const divOptions = document.querySelector('.options');
    // Verifica se o clique não foi dentro do menu de opções
    if (!event.target.closest('.options') && divOptions.style.display === 'block') {
        divOptions.style.display = 'none';
    }
}

// Adiciona o event listener que ao clicar em qualquer parte da tela(que não seja o menu), ele fecha as opções
document.addEventListener('click', hideOptions);


async function logout(event) {
    if(event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    console.log('Iniciando processo de logout');
    
    try {
        // 1. Limpa os dados locais primeiro
        localStorage.removeItem('usuario');
        localStorage.removeItem('token');
        
        // 2. Envia requisição para o servidor
        const response = await fetch('http://localhost:5000/logout', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Falha na resposta do servidor');
        }
        
        const data = await response.json();
        console.log('Resposta do logout:', data);
        
        // 3. Redireciona para a página inicial
        window.location.href = '../public/index.html';
        
    } catch (error) {
        console.error('Erro durante logout:', error);
        // Redireciona mesmo com erro (limpeza local já foi feita)
        window.location.href = '../public/index.html';
    } finally {
        document.querySelector('.options').style.display = 'none';
    }
}
