from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:3000"],
        "supports_credentials": True
    }
})

# Configurações do banco de dados (como dicionário)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'projeto_game',
}

#Teste de conexão com o bd
try:
    test_conn = mysql.connector.connect(**db_config)
    print(""
    ""
    "")
    print("Conexão com o MySQL estabelecida com sucesso!")
    print(""
    ""
    "")
    test_conn.close()
except Exception as e:
    print(""
    ""
    "")
    print(f"Erro ao conectar ao MySQL: {e}")
    print(""
    ""
    "")

G_email = ''

#ROTAS PARA CADASTRO DO USUÁRIO + INFORMAÇÕES PARA O PERFIL
#Rotas de login e logout
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.get_json()
        print("Dados recebidos:", dados)
        nome = dados['nome']
        email = dados['email']
        senha = dados['senha']
        print('Dados recebidos:', nome, email, senha)

        # Cria nova conexão usando o dicionário de configuração
        conexao = mysql.connector.connect(**db_config)
        print("Conexão bem-sucedida!")
        cursor = conexao.cursor()

        # Verifica se email já existe
        cursor.execute("SELECT id_usuario FROM Usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'message': 'Email já cadastrado'}), 400
        print("Email disponível!")

        # Insere novo usuário
        sql = "INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, senha))
        print("Usuário cadastrado com sucesso!")
        conexao.commit()

        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201

    except Exception as e:
        print("Erro completo:", str(e))
        return jsonify({'message': f'Erro no servidor: {str(e)}'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        dados = request.get_json()
        email = dados['email']
        senha = dados['senha']

        global G_email 

        G_email = email

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            "SELECT id_usuario, nome, senha FROM Usuario WHERE email = %s", 
            (email,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({'message': 'Credenciais inválidas'}), 401
            

        if usuario['senha'] != senha:
            return jsonify({'message': 'Credenciais inválidas'}), 401

        #Retorna ao frontend o id do usuário e o token para autenticação
        return jsonify({
            'message': 'Login bem-sucedido',
            'usuario': {
                'id': usuario['id_usuario'],
                'nome': usuario['nome']
            },
            'token': 'token_gerado'  
        }), 200

    except Exception as e:#tratamento de erros
        print("Erro no login:", str(e))
        return jsonify({'message': 'Erro no servidor'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


@app.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'preflight'}), 200
        
    try:
        response = jsonify({
            'message': 'Logout realizado com sucesso',
            'success': True
        })
        
        # Limpa cookies
        response.set_cookie('session_token', '', expires=0, httponly=True, secure=False)

        return response
        
    except Exception as e:
        print("Erro durante logout:", str(e))
        return jsonify({'message': 'Erro durante logout', 'success': False}), 500


#ROTAS DE VERIFICAÇÃO
@app.route('/check-apelido', methods=['GET'])
def check_apelido():
    try:
        usuario_id = request.args.get('usuario_id')
        
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)
        
        # Verifica se usuário já tem apelido
        cursor.execute("""
            SELECT apelido FROM Jogador 
            WHERE id_usuario = %s
        """, (usuario_id,))
        
        resultado = cursor.fetchone()
        
        # Retorna se tem ou nao apelido
        return jsonify({
            'temApelido': resultado is not None,
            'apelido': resultado['apelido'] if resultado else None
        })
        
    except Exception as e:
        print("Erro ao verificar apelido:", str(e))
        return jsonify({'message': 'Erro no servidor'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/registrar-apelido', methods=['POST'])
def registrar_apelido():
    try:
        dados = request.get_json()
        print(f"Dados recebidos: {dados}")  
        
        # Verifica se dados foram recebidos ou se os campos obrigatórios estão presentes
        if not dados or 'usuario_id' not in dados or 'apelido' not in dados:
            return jsonify({'success': False, 'message': 'Dados incompletos'}), 400

        usuario_id = dados['usuario_id']
        apelido = dados['apelido'].strip()
        
        if not apelido:
            return jsonify({'success': False, 'message': 'Apelido não pode ser vazio'}), 400

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        
        # Verifica se apelido já existe
        cursor.execute("SELECT id_jogador FROM Jogador WHERE apelido = %s", (apelido,))
        if cursor.fetchone():
            print(f"Apelido já existe: {apelido}")  
            return jsonify({
                'success': False,
                'message': 'Este apelido já está em uso'
            }), 400
        
        # Insere novo jogador
        cursor.execute(
            "INSERT INTO Jogador (apelido, id_usuario) VALUES (%s, %s)",
            (apelido, int(usuario_id))
        )
        
        conexao.commit()
        print(f"Apelido registrado com sucesso: {apelido} para usuário {usuario_id}")  # Log
        
        return jsonify({ #Retorna ao frontend o apelido registrado
            'success': True,
            'message': 'Apelido registrado com sucesso!',
            'apelido': apelido
        })
        
    except Exception as e: #tratamento de erros
        print(f"Erro completo ao registrar apelido: {str(e)}", flush=True)  # Log detalhado
        if 'conexao' in locals():
            conexao.rollback()
        return jsonify({
            'success': False,
            'message': f'Erro no servidor: {str(e)}'
        }), 500
    finally: #fechar conexão com o banco de dados se estiver aberta
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

#ROTAS DO PERFIL

#Rotas das infosrmações do usuario no perfil
@app.route('/perfil-usuario', methods=['GET'])
def perfil_usuario():
    try:
        usuario_id = request.args.get('usuario_id')
        
        if not usuario_id or not usuario_id.isdigit():
            return jsonify({'message': 'ID de usuário inválido'}), 400

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)
        
        # Busca informações do usuário
        cursor.execute("""
            SELECT u.nome, u.email, j.apelido 
            FROM Usuario u
            LEFT JOIN Jogador j ON u.id_usuario = j.id_usuario
            WHERE u.id_usuario = %s
        """, (int(usuario_id),))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'nome': resultado['nome'],
            'email': resultado['email'],
            'apelido': resultado['apelido']
        })
        
    except Exception as e:
        print(f"Erro ao buscar perfil: {str(e)}")
        return jsonify({'message': 'Erro no servidor'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


#Rota das configurações
@app.route('/verificar-email', methods=['POST'])
def verificar_email():
    try:
        dados = request.get_json()
        email = dados['email'].strip()
        usuario_id = dados.get('usuario_id')  # Verifica se 'usuario_id' foi fornecido
        
        if not email:
            return jsonify({'success': False, 'message': 'Email não pode ser vazio'}), 400

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)
        
        # Verifica se o email existe e pertence ao usuário (se usuario_id for fornecido)
        if usuario_id:
            cursor.execute("""
                SELECT id_usuario FROM Usuario 
                WHERE email = %s AND id_usuario = %s
            """, (email, int(usuario_id)))
        else:
            cursor.execute("SELECT id_usuario FROM Usuario WHERE email = %s", (email,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            return jsonify({
                'success': False,
                'message': 'Email não encontrado ou não corresponde ao usuário'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Email verificado com sucesso'
        })
        
    except Exception as e:
        print(f"Erro ao verificar email: {str(e)}")
        return jsonify({'message': 'Erro no servidor'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/alterar-senha', methods=['POST'])
def alterar_senha():
    try:
        dados = request.get_json()
        email = dados['email'].strip()
        nova_senha = dados['nova_senha'].strip()
        
        if not email or not nova_senha:
            return jsonify({'success': False, 'message': 'Dados incompletos'}), 400

        if len(nova_senha) < 6:
            return jsonify({'success': False, 'message': 'Senha deve ter pelo menos 6 caracteres'}), 400

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        
        # Atualiza a senha
        cursor.execute("""
            UPDATE Usuario SET senha = %s 
            WHERE email = %s
        """, (nova_senha, email))
        
        conexao.commit()
        
        return jsonify({
            'success': True,
            'message': 'Senha alterada com sucesso!'
        })
        
    except Exception as e:
        print(f"Erro ao alterar senha: {str(e)}")
        conexao.rollback()
        return jsonify({'message': 'Erro no servidor'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

#Rota de alteração do apelido
@app.route('/alterar-apelido-direto', methods=['POST'])
def alterar_apelido_direto():
    try:
        dados = request.get_json()
        usuario_id = dados['usuario_id']
        novo_apelido = dados['novo_apelido'].strip()
        
        if not novo_apelido:
            return jsonify({'success': False, 'message': 'Apelido não pode ser vazio'}), 400

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        
        # Atualiza o apelido diretamente sem verificar duplicatas
        cursor.execute("""
            UPDATE Jogador SET apelido = %s 
            WHERE id_usuario = %s
        """, (novo_apelido, int(usuario_id)))
        
        conexao.commit()
        
        return jsonify({
            'success': True,
            'message': 'Apelido atualizado com sucesso!',
            'novo_apelido': novo_apelido
        })
        
    except Exception as e:
        print(f"Erro ao alterar apelido: {str(e)}")
        conexao.rollback()
        return jsonify({'message': 'Erro no servidor'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


#Rota para a exclusão da conta
@app.route('/verificar-senha', methods=['POST'])
def verificar_senha():
    try:
        dados = request.get_json()
        usuario_id = dados['usuario_id']
        senha = dados['senha']
        
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT id_usuario FROM Usuario WHERE id_usuario = %s AND senha = %s", 
            (int(usuario_id), senha)
        )
        
        usuario = cursor.fetchone()
        
        if usuario:
            return jsonify({'success': True, 'message': 'Senha correta'}), 200
        else:
            return jsonify({'success': False, 'message': 'Senha incorreta'}), 401
            
    except Exception as e:
        print(f"Erro ao verificar senha: {str(e)}")
        return jsonify({'success': False, 'message': 'Erro no servidor'}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/deletar-conta', methods=['POST'])
def deletar_conta():
    try:
        dados = request.get_json()
        usuario_id = dados['usuario_id']
        
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        
        # Primeiro deleta o jogador (devido à foreign key)
        cursor.execute("DELETE FROM Jogador WHERE id_usuario = %s", (int(usuario_id),))
        
        # Depois deleta o usuário
        cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (int(usuario_id),))
        
        conexao.commit()
        
        print(f"Conta do usuário {usuario_id} deletada com sucesso")
        
        return jsonify({
            'success': True,
            'message': 'Conta deletada com sucesso'
        }), 200
        
    except Exception as e:
        print(f"Erro ao deletar conta: {str(e)}")
        if 'conexao' in locals() and conexao.is_connected():
            conexao.rollback()
        return jsonify({
            'success': False,
            'message': 'Erro ao deletar conta'
        }), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


#Rota de verificar se o usuario deseja que seu nome apareça no ranking de jogadores
@app.route('/atualizar-preferencia-tabela', methods=['POST'])
def atualizar_preferencia_tabela():
    try:
        dados = request.get_json()
        usuario_id = dados['usuario_id']
        mostrar_na_tabela = dados['mostrar_na_tabela']
        
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        
        cursor.execute("""
            UPDATE Jogador SET show_in_rank = %s 
            WHERE id_usuario = %s
        """, (mostrar_na_tabela, int(usuario_id)))
        
        conexao.commit()
        
        print(f"Preferência de tabela atualizada para usuário {usuario_id}: {mostrar_na_tabela}")
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f"Erro ao atualizar preferência de tabela: {str(e)}")
        conexao.rollback()
        return jsonify({'success': False}), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()



#ROTAS DO RANKING
@app.route('/ranking', methods=['GET'])
def obter_ranking():
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)
        
        # Obtém jogadores que optaram por aparecer no ranking, ordenados por record (menor tempo primeiro)
        # Se record for NULL ou jogadores empatarem, ordena por apelido
        cursor.execute("""
            SELECT apelido, record 
            FROM Jogador 
            WHERE show_in_rank = TRUE 
            ORDER BY 
                CASE WHEN record IS NULL THEN 1 ELSE 0 END,  -- Jogadores sem record vêm depois
                record ASC,  -- Menor tempo primeiro
                apelido ASC  -- Em caso de empate, ordena por apelido
        """)
        
        jogadores = cursor.fetchall()
        
        # Formata os dados para o frontend
        ranking = []
        for i, jogador in enumerate(jogadores):
            # Se não tiver record, mostra 0
            pontuacao = jogador['record'] if jogador['record'] else "0"
            ranking.append({
                'posicao': i + 1,
                'apelido': jogador['apelido'],
                'pontuacao': pontuacao
            })
        
        return jsonify({
            'success': True,
            'ranking': ranking
        }), 200
        
    except Exception as e:
        print(f"Erro ao obter ranking: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro ao obter ranking'
        }), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

# Rota para atualizar o record se for maior do que o que ja está armazenado
@app.route('/atualizar-record', methods=['POST'])
def atualizar_record():
    try:
        dados = request.get_json()
        usuario_id = dados['usuario_id']
        pontos = int(dados['pontos'])

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)
        
        # Verifica se o jogador existe e obtém o record atual
        cursor.execute("""
            SELECT record, apelido FROM Jogador 
            WHERE id_usuario = %s
        """, (usuario_id,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"Jogador não encontrado para o usuário ID: {usuario_id}")
            return jsonify({
                'success': False, 
                'message': 'Jogador não encontrado'
            }), 404

        record_atual = resultado['record'] if resultado['record'] is not None else 0
        apelido = resultado['apelido']
        
        print(f"Record atual para usuário {usuario_id} ({apelido}): {record_atual}")
        print(f"Pontuação recebida: {pontos}")

        # Atualiza apenas se a nova pontuação for maior
        if pontos > record_atual:
            print(f"Atualizando record para {pontos} (anterior: {record_atual})")
            cursor.execute("""
                UPDATE Jogador 
                SET record = %s 
                WHERE id_usuario = %s
            """, (pontos, usuario_id))
            
            conexao.commit()
            print("Record atualizado com sucesso no banco de dados")
            
            return jsonify({
                'success': True,
                'atualizado': True,
                'novo_record': pontos,
                'record_anterior': record_atual,
                'apelido': apelido
            })
        
        print("Pontuação não atualizada (menor que o record atual)")
        return jsonify({
            'success': True,
            'atualizado': False,
            'motivo': 'Pontuação menor que o record atual',
            'record_atual': record_atual,
            'pontuacao_enviada': pontos,
            'apelido': apelido
        })
        
    except Exception as e:
        print(f"Erro ao atualizar record: {str(e)}")
        return jsonify({
            'success': False, 
            'message': str(e)
        }), 500
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')