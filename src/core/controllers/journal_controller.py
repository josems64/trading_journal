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
        Recopila los datos del formulario, los procesa y los guarda en la base de datos.
        """
        try:
            # Reemplazar comas con puntos para la conversión a float
            entry_price_str = self.view.entry_price_input.text().replace(',', '.')
            stop_loss_str = self.view.stop_loss_input.text().replace(',', '.')
            take_profit_str = self.view.take_profit_input.text().replace(',', '.')
            exit_price_str = self.view.exit_price_input.text().replace(',', '.')
            size_str = self.view.size_input.text().replace(',', '.')

            trade_data = {
                'date': self.view.date_input.text(),
                'symbol': self.view.symbol_input.text(),
                'direction': self.view.direction_input.text(),
                'entry_price': float(entry_price_str),
                'stop_loss': float(stop_loss_str),
                'take_profit': float(take_profit_str),
                'exit_price': float(exit_price_str),
                'size': float(size_str),
                'notes': self.view.notes_input.text(),
                'strategy': self.view.strategy_input.text(), # Nuevo campo
                'risk_reward': self.view.risk_reward_input.text(), # Nuevo campo
            }

            # TODO: Implementar la lógica de cálculo para profit_loss
            # Por ahora, un valor fijo para la prueba
            trade_data['profit_loss'] = (trade_data['exit_price'] - trade_data['entry_price']) * trade_data['size']

            self.db_manager.add_trade(trade_data)
            print("Operación guardada exitosamente.")
            self.clear_form()

        except ValueError:
            print("Error: Asegúrate de que los precios, el tamaño y otros valores numéricos sean válidos.")
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