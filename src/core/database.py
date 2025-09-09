import sqlite3
import os

class DatabaseManager:
    """
    Gestor para la base de datos del diario de trading.

    Esta clase maneja la conexión, creación de tablas y operaciones CRUD
    (Crear, Leer, Actualizar, Borrar) para la base de datos SQLite.
    """
    
    def __init__(self, db_path='data/trading_journal.db'):
        """
        Inicializa el gestor de la base de datos.
        
        Args:
            db_path (str): Ruta al archivo de la base de datos.
        """
        self.db_path = db_path
        
        # Asegura que el directorio del archivo de la base de datos exista.
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        self.conn = None
        self.cursor = None
        self._create_table()

    def connect(self):
        """Establece una conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            self.conn = None  # Asegurar que conn es None si falla la conexión

    def disconnect(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()

    def _create_table(self):
        """
        Crea la tabla 'trades' si no existe.

        La tabla almacena los detalles de las operaciones de trading.
        """
        self.connect()
        if self.conn is None:
            return
        
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    size REAL NOT NULL,
                    profit_loss REAL,
                    notes TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.disconnect()

    def add_trade(self, trade: dict):
        """
        Inserta una nueva operación en la base de datos.

        Args:
            trade (dict): Un diccionario con los datos de la operación.
        """
        self.connect()
        if self.conn is None:
            return
            
        try:
            self.cursor.execute('''
                INSERT INTO trades (date, symbol, direction, entry_price, exit_price, size, profit_loss, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (trade['date'], trade['symbol'], trade['direction'], trade['entry_price'], 
                  trade['exit_price'], trade['size'], trade['profit_loss'], trade['notes']))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al agregar la operación: {e}")
        finally:
            self.disconnect()
            
    def get_all_trades(self) -> list:
        """
        Consulta y devuelve todas las operaciones de la base de datos.

        Returns:
            list: Una lista de tuplas, donde cada tupla representa una fila de la tabla 'trades'.
        """
        self.connect()
        if self.conn is None:
            return []
            
        try:
            self.cursor.execute("SELECT * FROM trades")
            trades = self.cursor.fetchall()
            return trades
        except sqlite3.Error as e:
            print(f"Error al consultar operaciones: {e}")
            return []
        finally:
            self.disconnect()

if __name__ == '__main__':
    # Este bloque solo se ejecutará cuando el script se ejecute directamente
    # como un módulo de prueba, no cuando se importe.
    db_manager = DatabaseManager()

    # Ejemplo de uso
    new_trade = {
        'date': '2025-09-07',
        'symbol': 'BTC',
        'direction': 'buy',
        'entry_price': 50000.0,
        'exit_price': 52000.0,
        'size': 0.1,
        'profit_loss': 200.0,
        'notes': 'Primera operación de prueba.'
    }
    db_manager.add_trade(new_trade)

    all_trades = db_manager.get_all_trades()
    print("\n--- Operaciones en la base de datos ---")
    for trade in all_trades:
        print(trade)