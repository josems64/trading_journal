import pytest
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.core.database import DatabaseManager
from src.ui.journal_view import JournalView

@pytest.fixture(scope="module")
def app():
    """Fixture para inicializar la aplicación de PyQt."""
    return QApplication([])

@pytest.fixture(scope="function")
def db_manager():
    """Fixture para crear un gestor de base de datos de prueba."""
    # Usar una base de datos temporal para las pruebas
    test_db_path = "test_trading_journal.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    manager = DatabaseManager(db_path=test_db_path)
    yield manager
    
    # Limpiar después de la prueba
    manager.disconnect()
    os.remove(test_db_path)

def test_save_trade_integration(app, db_manager):
    """
    Test de integración que verifica que el formulario guarda datos en la base de datos.
    """
    # 1. Instanciar la vista de registro
    journal_view = JournalView()
    
    # 2. Conectar la vista al gestor de la base de datos (simulando el controlador)
    journal_view.save_button.clicked.connect(lambda: db_manager.add_trade({
        'date': journal_view.date_input.text(),
        'symbol': journal_view.symbol_input.text(),
        'direction': journal_view.direction_input.text(),
        'entry_price': float(journal_view.entry_price_input.text().replace(',', '.')),
        'stop_loss': float(journal_view.stop_loss_input.text().replace(',', '.')) if journal_view.stop_loss_input.text() else None,
        'take_profit': float(journal_view.take_profit_input.text().replace(',', '.')) if journal_view.take_profit_input.text() else None,
        'exit_price': float(journal_view.exit_price_input.text().replace(',', '.')),
        'size': float(journal_view.size_input.text().replace(',', '.')),
        'profit_loss': 0, # Placeholder
        'notes': journal_view.notes_input.text(),
        'strategy': journal_view.strategy_input.text(),
        'risk_reward': float(journal_view.risk_reward_input.text().replace(',', '.')) if journal_view.risk_reward_input.text() else None
    }))

    # 3. Simular la entrada de datos por el usuario
    journal_view.date_input.setText("13/09/2025")
    journal_view.symbol_input.setText("BTC/USD")
    journal_view.direction_input.setText("long")
    journal_view.entry_price_input.setText("20000,00")
    journal_view.stop_loss_input.setText("19800")
    journal_view.take_profit_input.setText("21000")
    journal_view.exit_price_input.setText("20500")
    journal_view.size_input.setText("0,5")
    journal_view.notes_input.setText("Prueba de test")
    journal_view.strategy_input.setText("Scalping")
    journal_view.risk_reward_input.setText("2,5")
    
    # 4. Simular clic en el botón de guardar
    journal_view.save_button.click()
    
    # 5. Obtener los datos de la base de datos
    db_manager.connect()
    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT * FROM trades WHERE symbol='BTC/USD'")
    result = cursor.fetchone()
    db_manager.disconnect()
    
    # 6. Afirmaciones para verificar los resultados
    assert result is not None
    assert result[1] == "13/09/2025" # 'date'
    assert result[4] == 20000.00    # 'entry_price'
    assert result[5] == 19800.0     # 'stop_loss'
    assert result[6] == 21000.0     # 'take_profit'
    assert result[7] == 20500.0     # 'exit_price'
    assert result[8] == 0.5         # 'size'
    assert result[10] == "Prueba de test" # 'notes'
    assert result[11] == "Scalping" # 'strategy'
    assert result[12] == 2.5        # 'risk_reward'