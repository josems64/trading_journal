import os
import sqlite3
import pytest
from src.core.database import DatabaseManager

@pytest.fixture
def db_manager():
    """
    Fixture que crea y gestiona una base de datos de prueba para los tests.
    """
    test_db_path = os.path.join('data', 'test_trading_journal.db')
    
    # Asegúrate de que la carpeta 'data' exista
    os.makedirs('data', exist_ok=True)
    
    # Crea una instancia de DatabaseManager con una base de datos de prueba
    manager = DatabaseManager(test_db_path)
    
    # Retorna la instancia para que el test la use
    yield manager
    
    # Lógica de limpieza después de que el test ha terminado
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print(f"\nBase de datos de prueba eliminada: {test_db_path}")

def test_db_connection(db_manager):
    """
    Test para verificar que la conexión a la base de datos se establece correctamente.
    """
    try:
        db_manager.connect()
        assert db_manager.conn is not None
    finally:
        db_manager.disconnect()

def test_table_creation(db_manager):
    """
    Test para verificar que la tabla 'trades' se crea correctamente.
    """
    db_manager.connect()
    try:
        # Verificamos si la tabla 'trades' existe
        cursor = db_manager.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades';")
        assert cursor.fetchone() is not None
    finally:
        db_manager.disconnect()