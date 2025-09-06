import sqlite3
import os

class DatabaseManager:
    """
    Gestor para la base de datos del diario de trading.
    """
    
    def __init__(self, db_name='trading_journal.db'):
        # Ruta del archivo de la base de datos dentro de la carpeta 'data'
        self.db_path = os.path.join('data', db_name)
        # Asegúrate de que la carpeta 'data' exista
        os.makedirs('data', exist_ok=True)  # <-- Línea corregida
        
        self.conn = None
        self.cursor = None
        self._create_table()

    def connect(self):
        """Establece una conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos exitosa.")
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")

    def disconnect(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def _create_table(self):
        """Crea la tabla de operaciones si no existe."""
        self.connect()
        # Verificar si la conexión falló
        if self.conn is None:
            return  # Salir de la función si no hay conexión
        
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
            print("Tabla 'trades' verificada/creada exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            self.disconnect()

    def add_trade(self, trade):
        """
        Inserta una nueva operación en la base de datos.
        """
        self.connect()
        # Verificar si la conexión falló
        if self.conn is None:
            return
            
        try:
            self.cursor.execute('''
                INSERT INTO trades (date, symbol, direction, entry_price, exit_price, size, profit_loss, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (trade['date'], trade['symbol'], trade['direction'], trade['entry_price'], 
                  trade['exit_price'], trade['size'], trade['profit_loss'], trade['notes']))
            self.conn.commit()
            print("Operación agregada exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al agregar la operación: {e}")
        finally:
            self.disconnect()
            
    def get_all_trades(self):
        """
        Consulta y devuelve todas las operaciones de la base de datos.
        """
        self.connect()
        # Verificar si la conexión falló
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
    # Ejemplo de uso de la clase
    db_manager = DatabaseManager()

    # Agregar una nueva operación
    new_trade = {
        'date': '2025-09-04',
        'symbol': 'TSLA',
        'direction': 'buy',
        'entry_price': 250.50,
        'exit_price': 255.75,
        'size': 10,
        'profit_loss': 52.50,
        'notes': 'Operación de prueba.'
    }
    db_manager.add_trade(new_trade)

    # Consultar todas las operaciones
    all_trades = db_manager.get_all_trades()
    print("\n--- Operaciones en la base de datos ---")
    for trade in all_trades:
        print(trade)