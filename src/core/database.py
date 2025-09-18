import sqlite3
import os

class DatabaseManager:
    """
    Gestor de la base de datos SQLite para el diario de trading.
    """
    def __init__(self, db_path="data/trading_journal.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._create_directory()
        self._create_tables()

    def _create_directory(self):
        """
        Crea el directorio para la base de datos si no existe.
        """
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directorio '{directory}' creado exitosamente.")

    def connect(self):
        """
        Establece una conexión con la base de datos SQLite y crea un cursor.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            self.conn = None
            self.cursor = None

    def disconnect(self):
        """
        Cierra la conexión de la base de datos.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def _create_tables(self):
        """
        Crea todas las tablas necesarias si no existen.
        """
        self.connect()
        if self.conn is None:
            return

        try:
            # Crea la tabla 'users'
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT
                )
            ''')
            self.conn.commit()
            
            # Crea la tabla 'assets'
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            self.conn.commit()

            # Crea la tabla 'trades'
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    stop_loss REAL,
                    take_profit REAL,
                    exit_price REAL,
                    size REAL NOT NULL,
                    profit_loss_usd REAL,
                    notes TEXT,
                    strategy TEXT,
                    risk_reward REAL,
                    trade_outcome TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            self.conn.commit()
            
            print("Tablas 'users', 'assets' y 'trades' verificadas/creadas exitosamente.")

        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")
        finally:
            self.disconnect()

    def add_trade(self, trade_data):
        """
        Agrega una nueva operación a la tabla 'trades'.
        """
        self.connect()
        if self.conn is None:
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO trades (
                    user_id, date, time, symbol, direction, entry_price, stop_loss, take_profit,
                    exit_price, size, profit_loss_usd, notes,
                    strategy, risk_reward, trade_outcome
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_data.get('user_id'), trade_data.get('date'), trade_data.get('time'), trade_data.get('symbol'), trade_data.get('direction'),
                trade_data.get('entry_price'), trade_data.get('stop_loss'), trade_data.get('take_profit'),
                trade_data.get('exit_price'), trade_data.get('size'),
                trade_data.get('profit_loss_usd'), trade_data.get('notes'), trade_data.get('strategy'),
                trade_data.get('risk_reward'), trade_data.get('trade_outcome')
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")
        finally:
            self.disconnect()

    def get_assets_by_user(self, user_id):
        """
        Obtiene todos los activos registrados por un usuario.
        """
        self.connect()
        if self.conn is None:
            return []
        
        try:
            self.cursor.execute("SELECT name FROM assets WHERE user_id = ?", (user_id,))
            assets = [row[0] for row in self.cursor.fetchall()]
            return assets
        except sqlite3.Error as e:
            print(f"Error al obtener los activos: {e}")
            return []
        finally:
            self.disconnect()
