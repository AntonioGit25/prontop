import sqlite3

class DatabaseManager:
    """
    Gerencia as operações de banco de dados SQLite para o sistema de login.
    Utiliza parameterized queries para prevenir SQL injection.
    """

    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """
        Conecta-se ao banco de dados e cria a tabela 'users' se ela não existir.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """)
            conn.commit()

    def _get_connection(self):
        """
        Retorna uma conexão com o banco de dados.
        """
        return sqlite3.connect(self.db_path)

    def insert_user(self, username, password_hash):
        """
        Insere um novo usuário no banco de dados.
        Retorna True em caso de sucesso, False se o usuário já existir (username UNIQUE).
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Captura erro se o username já existir
            return False
        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
            return False

    def get_user_by_username(self, username):
        """
        Busca um usuário pelo nome de usuário.
        Retorna uma tupla (id, username, password_hash) se encontrado, ou None.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,)
            )
            return cursor.fetchone() # Retorna uma tupla ou None

    def close(self):
        """
        Método para fechar a conexão, embora o uso de 'with' a gerencie automaticamente.
        Adicionado por completude, se houver cenários onde uma conexão persistente seja usada.
        """
        # A conexão é fechada automaticamente pelo gerenciador de contexto 'with'
        pass