// Sobrescreve o console.log para capturar saídas específicas do Python
const originalConsoleLog = console.log;
console.log = (message) => {
  originalConsoleLog(message);
  
  // Filtra mensagens de vitória do jogo
  if (typeof message === 'string' && message.includes("VICTORY_DATA:")) {
    try {
      const dados = JSON.parse(message.split("VICTORY_DATA:")[1]);
      
      // Envia para o backend Flask
      fetch('http://localhost:5000/atualizar-record', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: dados.email,
          pontos: dados.pontos
        })
      })
      .then(response => response.json())
      .then(data => {
        console.log("Resposta do servidor:", data);
        if (data.success && data.atualizado) {
          // Atualiza a UI se necessário
          document.dispatchEvent(new CustomEvent('record-atualizado', {
            detail: data.novo_record
          }));
        }
      })
      .catch(error => {
        console.error("Erro ao enviar pontuação:", error);
      });
    } catch (e) {
      console.error("Erro ao processar mensagem do Python:", e);
    }
  }
};