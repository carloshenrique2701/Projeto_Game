# 🎮 Sussuros do labirinto - Projeto Integrado Web

**Descrição breve**: Um jogo 3D estilo Doom/Wolfenstein com raycasting, integrado a um sistema web com autenticação, ranking e perfil de usuário.


## 📌 Índice
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Funcionalidades](#-funcionalidades)
- [Jogo](#-Jogo)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desafios Técnicos](#-Desafios-Técnicos)
- [Créditos](#-Créditos)



## 🛠 Tecnologias Utilizadas
- **Frontend (Jogo)**: 

  - Python (Pygame, Pygbag)

  - Raycasting para gráficos 3D (inspirado no jogo Doom, Wolfenstein 3d, etc)

- **Backend**:

  - Python (Flask, Flask-CORS)

  - MySQL (mysql-connector)

- **Outros**:
  - OS/Sys para manipulação de arquivos


## 🎯 Funcionalidades
### 🔐 Autenticação
- Login/Cadastro

- Verificação de apelido único

- Alterar senha/apelido

- Deletar conta (com verificação de senha)

- Toggle para aparecer no ranking

- Visualização de informaçõesdo usuário em seu prefil


### 🏆 Ranking
- Lista de jogadores com pontuações(cosos de empate em pontuação, são desampatados em ordem alfabética)

- Filtro por visibilidade (usuários que optaram por aparecer)


## 🎮 Jogo
- Renderização 3D com raycasting

- Inimigos e sistema de colisão

- Sistema de pause

- Sistema de renderização de texturas, apartir da tecnica de percepção de raycasting

- Mapa 2d (50x50)

### 🎮 Níveis de Dificuldade (com frases de provocação)

| Dificuldade | 🎯 Inimigos | ❤️ Vida do Jogador | 💬Provacação                                                                    |
|-------------|-------------|--------------------|---------------------------------------------------------------------------------|
| Fácil  🌶️   | 150         | 200 HP             | "Deixa de ser fraco seu vacilão, põe pelo menos no normal. FRANGO!"             |
| Normal      | 200         | 200 HP             | "Você é um jogador normal que está em busca de novas experiências."             |
| Expert      | 250         | 150 HP             | "Você está se achando o melhor do mundo. Eu DUVIDO!"                            |
| Bruto       | 300         | 150 HP             | "De bruto tu não tem nada. Quando o teu fica na reta tu sai fora."              |
| Jiraya 🌶️🌶️ | 350         | 100 HP             | "Tá se achando, não vai aguentar nem 15 segundos e vai ficar chorando depois."  |


### 🤖 Inteligência Artificial
- Sistema de pathfinding:

        *Inimigos usam um algoritmo de "seguir o jogador" baseado em linha reta (line-of-sight).

        *Se o inimigo vê o jogador (sem obstruções), ele se move diretamente em direção a ele.

        *Se há obstáculos, o jogo usa um sistema de waypoints pré-definidos ou busca em largura (BFS) para navegar pelo mapa.


### ⚙️ Mecânicas Principais
- 3 tipos diferentes de NPCs inimigos (SoldierNPC, CacoDemonNPC, CyberDemonNPC) (78-220 pontos/kill)

- Sistema de interação com as paredes, onde gera pontos de forma aleatória(de 45 a 120)

- Sistema de recuperação de vida enquanto não está sendo atingido

- Sistema de disparo com delay para evitar diversos disparos consecutivos

- Sons e efeitos imersivos(thema feito em ia)

- Sistema de sprites estáticos e animados (bonecas e tochas)

- Pontuação integrada ao backend (mecanica de tempo ao finalizar o jogo, multiplica a pontuação)


### Controles

- `WASD` → Movimento
- `Mouse` → Mira/Disparo
- `Esc` → Pause
- `E` → Interações


## 🚀 Como Executar
### Pré-requisitos
- Python 3.10+

- MySQL instalado

- Bibliotecas listadas em `requirements.txt`

- Windows (necessario para instalar pygbag)

### Passo a Passo
1. **Clone o repositório**:
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd [NOME_DO_REPOSITORIO]

2. Instale o pygbag (necesario estar em Windows, pois essa biblioteca não tem suporte para Linux)
   ```bash
   pip install pygbag

3. Instale as bibliotecas listadas em `requirements.txt`

   ```bash
   pip install -r requirements.txt

4. Ao gerar um ariquivo "jogo.apk", mova ele para a pasta "frontend/jogo"

5. Ajuste as configurações do banco de dados no arquivo `backend/app.py` (host, user, password, database)

6. Inicie o servidor de desenvolvimento com o comando:
   ```bash
   python backend/app.py

7. Abra o navegador e navegue para http://localhost:5000

8. Crie uma conta ou faca login

9. Jogue!


## 📂 Estrutura do Projeto
```
Projeto_Game
├── backend
│   ├── app.py
│   └── database
│       └── database.sql
├── frontend
│   ├── jogo
│   │   ├── css
│   │   │   └── jogo.css
│   │   ├── imgs
│   │   │   └── perfil.png
│   │   ├── jogo.html
│   │   └── js
│   │       ├── pontuacao.js
│   │       ├── requisicao-Apelido.js
│   │       └── script.js
│   ├── perfil
│   │   ├── css
│   │   │   └── perfil.css
│   │   ├── imgs
│   │   │   └── perfil.png
│   │   ├── js
│   │   │   ├── configuracoes.js
│   │   │   └── infos.js
│   │   └── perfil.html
│   ├── public
│   │   ├── css
│   │   │   └── estilo.css
│   │   ├── gif
│   │   │   └── 0.gif
│   │   ├── index.html
│   │   └── js
│   │       └── inicial.js
│   └── ranking
│       ├── css
│       │   └── ranking.css
│       ├── js
│       │   └── ranking.js
│       └── ranking.html
├── Jogo
│   ├── main.py
│   ├── map.py
│   ├── menu.py
│   ├── npc.py
│   ├── object_handler.py
│   ├── object_render.py
│   ├── pathfinding.py
│   ├── pause_menu.py
│   ├── player.py
│   ├── raycasting.py
│   ├── resources
│   │   ├── fonts
│   │   │   ├── resto.ttf
│   │   │   └── titulo.ttf
│   │   ├── sound
│   │   │   ├── npc_attack.wav
│   │   │   ├── npc_death.wav
│   │   │   ├── npc_pain.wav
│   │   │   ├── player_pain.wav
│   │   │   ├── shotgun.wav
│   │   │   └── themes
│   │   │       └── 0.mp3
│   │   ├── sprites
│   │   │   ├── animated_sprites
│   │   │   │   └── tochas
│   │   │   │       ├── 0.png
│   │   │   │       ├── 1.png
│   │   │   │       ├── 2.png
│   │   │   │       ├── 3.png
│   │   │   │       ├── 4.png
│   │   │   │       ├── 5.png
│   │   │   │       └── 6.png
│   │   │   ├── npc
│   │   │   │   ├── caco_demon
│   │   │   │   │   ├── 0.png
│   │   │   │   │   ├── attack
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   ├── 1.png
│   │   │   │   │   │   ├── 2.png
│   │   │   │   │   │   ├── 3.png
│   │   │   │   │   │   └── 4.png
│   │   │   │   │   ├── death
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   ├── 1.png
│   │   │   │   │   │   ├── 2.png
│   │   │   │   │   │   ├── 3.png
│   │   │   │   │   │   ├── 4.png
│   │   │   │   │   │   └── 5.png
│   │   │   │   │   ├── idle
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   ├── 1.png
│   │   │   │   │   │   ├── 2.png
│   │   │   │   │   │   ├── 3.png
│   │   │   │   │   │   ├── 4.png
│   │   │   │   │   │   ├── 5.png
│   │   │   │   │   │   ├── 6.png
│   │   │   │   │   │   └── 7.png
│   │   │   │   │   ├── pain
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   └── 1.png
│   │   │   │   │   └── walk
│   │   │   │   │       ├── 0.png
│   │   │   │   │       ├── 1.png
│   │   │   │   │       └── 2.png
│   │   │   │   ├── cyber_demon
│   │   │   │   │   ├── 0.png
│   │   │   │   │   ├── attack
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   └── 1.png
│   │   │   │   │   ├── death
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   ├── 1.png
│   │   │   │   │   │   ├── 2.png
│   │   │   │   │   │   ├── 3.png
│   │   │   │   │   │   ├── 4.png
│   │   │   │   │   │   ├── 5.png
│   │   │   │   │   │   ├── 6.png
│   │   │   │   │   │   ├── 7.png
│   │   │   │   │   │   └── 8.png
│   │   │   │   │   ├── idle
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   ├── 1.png
│   │   │   │   │   │   ├── 2.png
│   │   │   │   │   │   ├── 3.png
│   │   │   │   │   │   ├── 4.png
│   │   │   │   │   │   ├── 5.png
│   │   │   │   │   │   ├── 6.png
│   │   │   │   │   │   └── 7.png
│   │   │   │   │   ├── pain
│   │   │   │   │   │   ├── 0.png
│   │   │   │   │   │   └── 1.png
│   │   │   │   │   └── walk
│   │   │   │   │       ├── 0.png
│   │   │   │   │       ├── 1.png
│   │   │   │   │       ├── 3.png
│   │   │   │   │       └── 4.png
│   │   │   │   └── soldier
│   │   │   │       ├── 0.png
│   │   │   │       ├── attack
│   │   │   │       │   ├── 0.png
│   │   │   │       │   └── 1.png
│   │   │   │       ├── death
│   │   │   │       │   ├── POSSM0.png
│   │   │   │       │   ├── POSSN0.png
│   │   │   │       │   ├── POSSO0.png
│   │   │   │       │   ├── POSSP0.png
│   │   │   │       │   ├── POSSQ0.png
│   │   │   │       │   ├── POSSR0.png
│   │   │   │       │   ├── POSSS0.png
│   │   │   │       │   ├── POSST0.png
│   │   │   │       │   └── POSSU0.png
│   │   │   │       ├── idle
│   │   │   │       │   ├── 0.png
│   │   │   │       │   ├── 1.png
│   │   │   │       │   ├── 2.png
│   │   │   │       │   ├── 3.png
│   │   │   │       │   ├── 4.png
│   │   │   │       │   ├── 5.png
│   │   │   │       │   ├── 6.png
│   │   │   │       │   └── 7.png
│   │   │   │       ├── pain
│   │   │   │       │   └── 0.png
│   │   │   │       └── walk
│   │   │   │           ├── 0.png
│   │   │   │           ├── 1.png
│   │   │   │           ├── 2.png
│   │   │   │           └── 3.png
│   │   │   ├── static_sprites
│   │   │   │   └── boneca.png
│   │   │   └── weapon
│   │   │       ├── 0.png
│   │   │       ├── 1.png
│   │   │       ├── 2.png
│   │   │       ├── 3.png
│   │   │       ├── 4.png
│   │   │       └── 5.png
│   │   └── textures
│   │       ├── 1.png
│   │       ├── 5.png
│   │       ├── 6.png
│   │       ├── 7.png
│   │       ├── 9.png
│   │       ├── blood_screen.png
│   │       ├── digits
│   │       │   ├── 0.png
│   │       │   ├── 10.png
│   │       │   ├── 1.png
│   │       │   ├── 2.png
│   │       │   ├── 3.png
│   │       │   ├── 4.png
│   │       │   ├── 5.png
│   │       │   ├── 6.png
│   │       │   ├── 7.png
│   │       │   ├── 8.png
│   │       │   └── 9.png
│   │       └── game_over.png
│   ├── settings.py
│   ├── sound.py
│   ├── sprite_object.py
│   ├── victory.py
│   └── weapon.py
├── README
└── requirements.txt
```

## 🧠 Desafios Técnicos
- Otimização do raycasting para evitar lag em mapas grandes.

- Sincronização do ranking em tempo real com o backend.

- Pathfinding dos NPCs em mapas labirínticos.

- Captura da pontuação de um arquivo .apk para ser enviado ao backend.

- Otimização dos sprites para melhorar a performance na web.

- Implementação na web.

- Recorte, remoção de fundo e organização das pastas para cada sprite de NPCs inimigo.

- Criação de uma animação sprite/sprite.

- Renderização de texturas.


## Créditos

- [spriters-resource](https://www.spriters-resource.com/search/?q=doom)(https://spritedatabase.net/game/760)
- [Thema-Music](https://suno.com/home)