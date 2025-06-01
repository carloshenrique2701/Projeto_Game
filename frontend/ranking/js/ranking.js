document.addEventListener('DOMContentLoaded', () => {
    carregarRanking();
});

async function carregarRanking() {
    try {
        const response = await fetch('http://localhost:5000/ranking');
        const data = await response.json();
        
        if (data.success) {
            preencherTabela(data.ranking);
        } else {
            console.error('Erro ao carregar ranking:', data.message);
            mostrarMensagemErro();
        }
    } catch (error) {
        console.error('Erro:', error);
        mostrarMensagemErro();
    }
}

function preencherTabela(ranking) {
    const tbody = document.querySelector('.ranking-table tbody');
    tbody.innerHTML = ''; // Limpa a tabela
    
    if (ranking.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td colspan="3" class="sem-dados">Nenhum jogador no ranking ainda</td>`;
        tbody.appendChild(tr);
        return;
    }
    
    ranking.forEach(jogador => {
        const tr = document.createElement('tr');
        
        // Adiciona classe especial para os 3 primeiros
        if (jogador.posicao <= 3) {
            tr.classList.add(`top-${jogador.posicao}`);
        }
        
        tr.innerHTML = `
            <td>${jogador.posicao}</td>
            <td>${jogador.apelido}</td>
            <td>${jogador.pontuacao}</td>
        `;
        
        tbody.appendChild(tr);
    });
}

function mostrarMensagemErro() {
    const tbody = document.querySelector('.ranking-table tbody');
    tbody.innerHTML = `
        <tr>
            <td colspan="3" class="erro-carregamento">
                Erro ao carregar ranking. Tente recarregar a página.
            </td>
        </tr>
    `;
}