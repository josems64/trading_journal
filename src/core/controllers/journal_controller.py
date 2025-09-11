from src.core.database import DatabaseManager

class JournalController:
    """
    Controlador para la vista de registro de operaciones.
    """
    def __init__(self, view, db_manager):
        """
        Inicializa el controlador.

        Args:
            view: La instancia de la vista JournalView.
            db_manager: La instancia de DatabaseManager.
        """
        self.view = view
        self.db_manager = db_manager
        self.connect_signals()

    def connect_signals(self):
        """
        Conecta las señales de la vista con los métodos del controlador.
        """
        self.view.save_button.clicked.connect(self.save_trade)

    def save_trade(self):
        """
        Recopila los datos del formulario y los guarda en la base de datos.
        """
        try:
            trade_data = {
                'date': self.view.date_input.text(),
                'symbol': self.view.symbol_input.text(),
                'direction': self.view.direction_input.text(),
                'entry_price': float(self.view.entry_price_input.text()),
                'stop_loss': float(self.view.stop_loss_input.text()),
                'take_profit': float(self.view.take_profit_input.text()),
                'exit_price': float(self.view.exit_price_input.text()),
                'size': float(self.view.size_input.text()),
                'notes': self.view.notes_input.text()
            }
            
            # TODO: Implementar la lógica de cálculo para profit_loss
            # Por ahora, un valor fijo para la prueba
            trade_data['profit_loss'] = trade_data['exit_price'] - trade_data['entry_price']

            self.db_manager.add_trade(trade_data)
            print("Operación guardada exitosamente.")
            self.clear_form()

        except ValueError:
            print("Error: Asegúrate de que los precios y el tamaño sean números válidos.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def clear_form(self):
        """
        Limpia todos los campos del formulario.
        """
        self.view.date_input.clear()
        self.view.symbol_input.clear()
        self.view.direction_input.clear()
        self.view.entry_price_input.clear()
        self.view.stop_loss_input.clear()
        self.view.take_profit_input.clear()
        self.view.exit_price_input.clear()
        self.view.size_input.clear()
        self.view.notes_input.clear()