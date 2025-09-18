import bcrypt
import sqlite3
from src.core.database import DatabaseManager

class AuthService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def hash_password(self, password):
        """Cifra la contraseña usando bcrypt."""
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode('utf-8')

    def check_password(self, password, hashed_password):
        """Verifica si la contraseña coincide con el hash."""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def register_user(self, username, password, first_name, last_name, email):
        """Registra un nuevo usuario en la base de datos con los nuevos campos."""
        self.db_manager.connect()
        if self.db_manager.conn is None:
            return False, "Error de conexión con la base de datos."
        
        try:
            hashed_password = self.hash_password(password)
            self.db_manager.cursor.execute(
                "INSERT INTO users (username, password_hash, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                (username, hashed_password, first_name, last_name, email)
            )
            user_id = self.db_manager.cursor.lastrowid
            self.db_manager.conn.commit()
            
            self._add_initial_assets(user_id)
            
            return True, "Usuario registrado exitosamente."
        except sqlite3.IntegrityError:
            return False, "Ese nombre de usuario ya existe."
        except Exception as e:
            return False, f"Error al registrar el usuario: {e}"
        finally:
            self.db_manager.disconnect()

    def login_user(self, username, password):
        """Verifica las credenciales del usuario y retorna el user_id si es válido."""
        self.db_manager.connect()
        if self.db_manager.conn is None:
            return None, "Error de conexión con la base de datos."
        
        try:
            self.db_manager.cursor.execute(
                "SELECT id, password_hash FROM users WHERE username = ?",
                (username,)
            )
            result = self.db_manager.cursor.fetchone()
            
            if result:
                user_id, hashed_password = result
                if self.check_password(password, hashed_password):
                    return user_id, "Inicio de sesión exitoso."
                else:
                    return None, "Contraseña incorrecta."
            else:
                return None, "Usuario no encontrado."
        except Exception as e:
            return None, f"Error al iniciar sesión: {e}"
        finally:
            self.db_manager.disconnect()

    def get_user_info(self, user_id):
        """Obtiene la información de un usuario por su ID."""
        self.db_manager.connect()
        if self.db_manager.conn is None:
            return None
        
        try:
            self.db_manager.cursor.execute(
                "SELECT username, first_name, last_name FROM users WHERE id = ?",
                (user_id,)
            )
            user_info = self.db_manager.cursor.fetchone()
            if user_info:
                return {
                    "username": user_info[0],
                    "first_name": user_info[1],
                    "last_name": user_info[2]
                }
            return None
        except Exception as e:
            print(f"Error al obtener información del usuario: {e}")
            return None
        finally:
            self.db_manager.disconnect()

    def _add_initial_assets(self, user_id):
        """Agrega activos predefinidos al registrar un nuevo usuario."""
        initial_assets = ["EUR/USD", "USD/JPY", "XAU/USD"]
        try:
            for asset in initial_assets:
                self.db_manager.cursor.execute(
                    "INSERT INTO assets (name, user_id) VALUES (?, ?)",
                    (asset, user_id)
                )
            self.db_manager.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar activos iniciales: {e}")