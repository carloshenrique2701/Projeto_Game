# backend/database/database.py
import mysql.connector
from mysql.connector import Error
import bcrypt

class DatabaseManager:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'sua_senha_aqui',  # <<< ALTERE
            'database': 'sistema_usuarios'
        }
        self.create_database_and_tables()

    def get_connection(self):
        """Estabelece conexão com o banco de dados"""
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def create_database_and_tables(self):
        """Cria o banco de dados e tabelas se não existirem"""
        try:
            # Conexão sem especificar o database inicialmente
            temp_config = self.config.copy()
            temp_config.pop('database')
            
            conn = mysql.connector.connect(**temp_config)
            cursor = conn.cursor()
            
            # Cria o database se não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            
            # Seleciona o database
            cursor.execute(f"USE {self.config['database']}")
            
            # Cria tabela de usuários
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL,
                data_nascimento DATE NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_login TIMESTAMP NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Cria tabela de pontuações (exemplo para o jogo)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pontuacoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                pontuacao INT NOT NULL,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
            """)
            
            # Insere um usuário admin padrão (opcional)
            senha_admin = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
            cursor.execute("""
            INSERT IGNORE INTO usuarios (nome, email, senha, data_nascimento)
            VALUES (%s, %s, %s, %s)
            """, ("Admin", "admin@game.com", senha_admin.decode('utf-8'), "2000-01-01"))
            
            conn.commit()
            print("✅ Banco de dados e tabelas verificados/criados com sucesso!")
            
        except Error as e:
            print(f"❌ Erro ao configurar o banco: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# Teste a conexão quando o arquivo é executado diretamente
if __name__ == "__main__":
    db = DatabaseManager()
    conn = db.get_connection()
    if conn:
        print("Conexão com o banco estabelecida com sucesso!")
        conn.close()
