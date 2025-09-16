from PyQt6.QtCore import QDate
from src.core.database import DatabaseManager
from src.ui.journal_view import JournalView
from src.ui.dashboard_view import DashboardView
from src.core.services.analysis_service import AnalysisService
from src.ui.dashboard_view import DashboardView
from src.core.services.analysis_service import AnalysisService


class JournalController:
    """
    Controlador para la vista de registro de operaciones.
    """
    
    def __init__(self, view: JournalView, db_manager: DatabaseManager, dashboard_view: DashboardView, analysis_service: AnalysisService):
        self.view = view
        self.db_manager = db_manager
        self.dashboard_view = dashboard_view
        self.analysis_service = analysis_service
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
            entry_price_str = self.view.entry_price_input.text().replace(',', '.')
            stop_loss_str = self.view.stop_loss_input.text().replace(',', '.')
            take_profit_str = self.view.take_profit_input.text().replace(',', '.')
            exit_price_str = self.view.exit_price_input.text().replace(',', '.')
            size_str = self.view.size_input.text().replace(',', '.')
            risk_reward_str = self.view.risk_reward_input.text().replace(',', '.')

            # 1. Validación de campos vacíos para valores numéricos
            if not all([entry_price_str, exit_price_str, size_str]):
                raise ValueError("Los campos de precio de entrada, precio de salida y tamaño no pueden estar vacíos.")

            # 2. Convertir los datos a sus tipos de dato correctos
            trade_data = {
                'date': self.view.date_input.text(),
                'symbol': self.view.symbol_input.text(),
                'direction': self.view.direction_input.currentText(),
                'entry_price': float(entry_price_str),
                'stop_loss': float(stop_loss_str) if stop_loss_str else None,
                'take_profit': float(take_profit_str) if take_profit_str else None,
                'exit_price': float(exit_price_str),
                'size': float(size_str),
                'notes': self.view.notes_input.text(),
                'strategy': self.view.strategy_input.text(),
                'risk_reward': float(risk_reward_str) if risk_reward_str else None,
            }

            # 3. Lógica de cálculo (como la definimos anteriormente)
            if trade_data['direction'].lower() == 'buy':
                profit_loss_points = (trade_data['exit_price'] - trade_data['entry_price'])
            else:
                profit_loss_points = (trade_data['entry_price'] - trade_data['exit_price'])

            # 4. Asignar el resultado y calcular la ganancia/pérdida en USD
            if profit_loss_points > 0:
                trade_outcome = "Win"
            elif profit_loss_points < 0:
                trade_outcome = "Loss"
            else:
                trade_outcome = "Breakeven"

            pip_value_usd = 10.0
            profit_loss_usd = profit_loss_points * trade_data['size'] * pip_value_usd

            trade_data['profit_loss'] = profit_loss_points
            trade_data['profit_loss_usd'] = profit_loss_usd
            trade_data['trade_outcome'] = trade_outcome

            # 5. Guardar los datos y limpiar el formulario
            self.db_manager.add_trade(trade_data)
            self.clear_form()
            self.update_dashboard() # <-- ¡Añade esta línea!

        except ValueError as e:
            print(f"Error: {e}")
            print("Asegúrate de que los precios, el tamaño y otros valores numéricos sean válidos.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
   
    def clear_form(self):
        """
        Limpia todos los campos del formulario de la vista.
        """
        self.view.date_input.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        self.view.symbol_input.clear()
        self.view.direction_input.setCurrentIndex(0)
        self.view.entry_price_input.clear()
        self.view.stop_loss_input.clear()
        self.view.take_profit_input.clear()
        self.view.exit_price_input.clear()
        self.view.size_input.clear()
        self.view.notes_input.clear()
        self.view.strategy_input.clear()
        self.view.risk_reward_input.clear()

    def update_dashboard(self):
        """
        Actualiza los datos mostrados en el dashboard de análisis.
        """
        # Obtenemos las metricas del servicio de analisis
        metrics = self.analysis_service.get_key_metrics()
        
        # Le decimos al dashboard que muestre las metricas
        self.dashboard_view.update_metrics(metrics)


    