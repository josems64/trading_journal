from PyQt6.QtCore import QDate, QObject
from PyQt6.QtWidgets import QMessageBox
from src.core.database import DatabaseManager
from src.ui.journal_view import JournalView
from src.ui.dashboard_view import DashboardView
from src.core.services.analysis_service import AnalysisService

class JournalController(QObject):
    def __init__(self, view: JournalView, db_manager: DatabaseManager, dashboard_view: DashboardView, analysis_service: AnalysisService):
        super().__init__()
        self.view = view
        self.db_manager = db_manager
        self.dashboard_view = dashboard_view
        self.analysis_service = analysis_service
        self.user_id = None
        self.connect_signals()
    
    def connect_signals(self):
        self.view.save_button.clicked.connect(self.save_trade)
        self.view.clear_button.clicked.connect(self.view.clear_form)

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.load_assets()

    def load_assets(self):
        assets = self.db_manager.get_assets_by_user(self.user_id)
        self.view.set_symbols(assets)

    def save_trade(self):
        trade_data = self.view.get_form_data()
    
        # Asigna el user_id para que se guarde en la base de datos
        trade_data['user_id'] = self.user_id

        # Validar campos obligatorios
        if not trade_data['symbol'] or not trade_data['direction'] or not trade_data['entry_price']:
            QMessageBox.warning(self.view, "Error de Entrada", "Por favor, completa los campos obligatorios: Símbolo, Tendencia y Precio de Entrada.")
            return

        # Validar y convertir campos numéricos
        try:
            trade_data['entry_price'] = float(trade_data['entry_price'])
            trade_data['stop_loss'] = float(trade_data['stop_loss']) if trade_data['stop_loss'] else None
            trade_data['take_profit'] = float(trade_data['take_profit']) if trade_data['take_profit'] else None
            trade_data['exit_price'] = float(trade_data['exit_price']) if trade_data['exit_price'] else None
            trade_data['size'] = float(trade_data['size'])
            trade_data['profit_loss_usd'] = float(trade_data['profit_loss_usd']) if trade_data['profit_loss_usd'] else 0.0
        except ValueError:
            QMessageBox.warning(self.view, "Error de Entrada", "Por favor, introduce valores numéricos válidos en los campos de precios, tamaño y P&L.")
            return

        # Determinar el resultado de la operación
        if trade_data['profit_loss_usd'] > 0:
            trade_data['trade_outcome'] = 'Win'
        elif trade_data['profit_loss_usd'] < 0:
            trade_data['trade_outcome'] = 'Loss'
        else:
            trade_data['trade_outcome'] = 'Break Even'

        # Guardar la operación en la base de datos
        self.db_manager.add_trade(trade_data)
        QMessageBox.information(self.view, "Éxito", "Operación guardada correctamente.")
        self.view.clear_form()
        self.update_dashboard()

    def update_dashboard(self):
        if self.user_id is None:
            return
        
        total_trades = self.analysis_service.get_total_trades(self.user_id)
        win_rate = self.analysis_service.get_win_rate(self.user_id)
        total_profit = self.analysis_service.get_total_profit(self.user_id)

        self.dashboard_view.update_stats({
            'total_trades': total_trades,
            'win_rate': f'{win_rate:.2f}%',
            'total_profit': f'{total_profit:.2f}'
        })


    