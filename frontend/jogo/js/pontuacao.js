// Variável global para armazenar a pontuação
let pontuacaoJogador = null;
let terminalObserver = null;

// Função para capturar os prints do terminal Python
function monitorarTerminalPython() {
    const terminal = document.getElementById('terminal');
    
    // Configura um MutationObserver para monitorar mudanças no terminal
    terminalObserver = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                const texto = node.textContent || node.innerText;
                
                // Procura pelo padrão "Pontuação = XXXX" nos prints
                const match = texto.match(/Pontuação\s*=\s*(\d+)/);
                if (match && match[1]) {
                    pontuacaoJogador = parseInt(match[1]);
                    console.log('Pontuação capturada:', pontuacaoJogador);
                    
                    // Mostra a pontuação na página para debug
                    document.getElementById('debug-output').textContent = 
                        `Pontuação capturada: ${pontuacaoJogador}`;
                    
                    // Envia para o backend (opcional)
                    enviarPontuacaoParaBackend(pontuacaoJogador);
                }
            });
        });
    });

    // Inicia a observação do terminal
    terminalObserver.observe(terminal, {
        childList: true,
        subtree: true
    });
}

// Função para enviar a pontuação para o backend
function enviarPontuacaoParaBackend(pontos) {
    console.log('Iniciando envio da pontuação para o backend...');
    
    // Obtém o usuário do localStorage (mesmo método usado no seu código)
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    if (!usuario || !usuario.id) {
        console.error('Erro: Usuário não está logado ou ID não disponível');
        document.getElementById('debug-output').textContent = 
            'Erro: Usuário não está logado. Pontuação não enviada.';
        return;
    }

    console.log(`Preparando para enviar pontuação: ${pontos} para o usuário ID: ${usuario.id}`);
    
    // Envia a requisição para o backend
    fetch('http://localhost:5000/atualizar-record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            usuario_id: usuario.id,  // Usando usuario.id em vez de email
            pontos: pontos
        })
    })
    .then(response => {
        console.log('Resposta recebida do servidor, status:', response.status);
        return response.json();
    })
    .then(data => {
        if (data.success) {
            if (data.atualizado) {
                console.log('Record atualizado com sucesso! Novo record:', data.novo_record);
                document.getElementById('debug-output').textContent = 
                    `🎉 Novo record registrado: ${data.novo_record}`;
                
                // Atualiza o record no objeto do usuário no localStorage se necessário
                usuario.record = data.novo_record;
                localStorage.setItem('usuario', JSON.stringify(usuario));
            } else {
                console.log('Pontuação não atualizada. Motivo:', data.motivo);
                document.getElementById('debug-output').textContent = 
                    `Pontuação atual: ${data.record_atual} (sua pontuação: ${pontos})`;
            }
        } else {
            console.error('Erro no servidor:', data.message);
            document.getElementById('debug-output').textContent = 
                'Erro ao atualizar record: ' + (data.message || 'Erro desconhecido');
        }
    })
    .catch(error => {
        console.error('Erro ao enviar pontuação:', error);
        document.getElementById('debug-output').textContent = 
            'Falha na conexão com o servidor. Tente novamente.';
    });
}

// Inicia o monitoramento quando a página estiver carregada
document.addEventListener('DOMContentLoaded', () => {
    // Espera o WASM carregar
    const checkReady = setInterval(() => {
        if (document.getElementById('terminal')) {
            clearInterval(checkReady);
            monitorarTerminalPython();
            
            // Adiciona um aviso visual
            const debugDiv = document.getElementById('debug-output');
            debugDiv.style.color = 'white';
            debugDiv.style.fontSize = '18px';
            debugDiv.textContent = 'Monitorando pontuação...';
        }
    }, 500);
});

