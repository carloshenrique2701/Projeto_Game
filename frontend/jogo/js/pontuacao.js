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
                    
                    // Envia para o backend
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
// Inicia o monitoramento quando a página estiver carregada
document.addEventListener('DOMContentLoaded', () => {
    // Espera o WASM carregar
    const checkReady = setInterval(() => {
        if (document.getElementById('terminal')) {
            clearInterval(checkReady);
            monitorarTerminalPython();
        }
    }, 500);
});

// Função para enviar a pontuação para o backend
function enviarPontuacaoParaBackend(pontos) {
    console.log('Iniciando envio da pontuação para o backend...');
    
    // Obtém o usuário do localStorage 
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    if (!usuario || !usuario.id) {
        console.error('Erro: Usuário não está logado ou ID não disponível');
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
            usuario_id: usuario.id, 
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
                
                // Atualiza o record no objeto do usuário no localStorage se necessário
                usuario.record = data.novo_record;
                localStorage.setItem('usuario', JSON.stringify(usuario));
            } else {
                console.log('Pontuação não atualizada. Motivo:', data.motivo);
            }
        } else {
            console.error('Erro no servidor:', data.message);
        }
    })
    .catch(error => {
        console.error('Erro ao enviar pontuação:', error);
    });
}


