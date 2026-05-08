import bcrypt

        def hash_password(password: str) -> bytes:
            """
            Gera um hash bcrypt para a senha fornecida.
            O salt é gerado automaticamente e incluído no hash.
            """
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return hashed_password

        def check_password(password: str, hashed_password: bytes) -> bool:
            """
            Verifica se a senha fornecida corresponde ao hash armazenado.
            """
            try:
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
            except ValueError:
                # Caso o hash_password não seja um hash bcrypt válido
                return False