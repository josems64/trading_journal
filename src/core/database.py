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
        self._create_table()

    def _create_directory(self):
        """
        Crea el directorio para la base de datos si no existe.
        """
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def connect(self):
        """
        Establece una conexión con la base de datos SQLite y crea un cursor.
        """
        try:
            # Imprimimos la ruta para verificar que sea correcta
            print(f"Intentando conectar a la base de datos en: {self.db_path}")
            
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos exitosa.")
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

    def _create_table(self):
        """
        Crea la tabla 'trades' si no existe.
        """
        self.connect()
        if self.conn is None:
            print("No se pudo conectar a la base de datos, no se creará la tabla.")
            return

        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    stop_loss REAL,
                    take_profit REAL,
                    exit_price REAL,
                    size REAL NOT NULL,
                    profit_loss REAL,
                    profit_loss_usd REAL,
                    notes TEXT,
                    strategy TEXT,
                    risk_reward REAL,
                    trade_outcome TEXT
                )
            ''')
            self.conn.commit()
            print("Tabla 'trades' verificada/creada exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
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
                    date, symbol, direction, entry_price, stop_loss, take_profit,
                    exit_price, size, profit_loss, profit_loss_usd, notes,
                    strategy, risk_reward, trade_outcome
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_data.get('date'), trade_data.get('symbol'), trade_data.get('direction'),
                trade_data.get('entry_price'), trade_data.get('stop_loss'), trade_data.get('take_profit'),
                trade_data.get('exit_price'), trade_data.get('size'), trade_data.get('profit_loss'),
                trade_data.get('profit_loss_usd'), trade_data.get('notes'), trade_data.get('strategy'),
                trade_data.get('risk_reward'), trade_data.get('trade_outcome')
            ))
            self.conn.commit()
            print("Datos insertados exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")
        finally:
            self.disconnect()