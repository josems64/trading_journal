# Abre src/ui/main_window.py

import sys
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QApplication, QLabel, QHBoxLayout, QWidget, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from src.ui.journal_view import JournalView
from src.ui.dashboard_view import DashboardView
from src.ui.maintenance_view import MaintenanceView
from src.core.controllers.journal_controller import JournalController
from src.core.controllers.maintenance_controller import MaintenanceController
from src.core.database import DatabaseManager
from src.core.services.analysis_service import AnalysisService
from src.core.services.maintenance_service import MaintenanceService
from src.core.services.auth_service import AuthService

class MainWindow(QMainWindow):
    def __init__(self, user_id, db_manager: DatabaseManager):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
        self.setWindowTitle("Trading Journal Pro")
        self.setGeometry(100, 100, 900, 600)
        self.user_id = user_id
        self.db_manager = db_manager

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.auth_service = AuthService(self.db_manager)
        self.setup_ui()

    def setup_ui(self):
        # Contenedor principal
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Header con el nombre de usuario
        header_layout = QHBoxLayout()
        user_info = self.auth_service.get_user_info(self.user_id)
        if user_info:
            full_name = f"{user_info['first_name']} {user_info['last_name']}"
            username_label = QLabel(f"{full_name} ({user_info['username']})")
            username_label.setFont(QFont("Arial", 14))
            username_label.setStyleSheet("color: #4A90E2;")
            header_layout.addWidget(username_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        main_layout.addLayout(header_layout)
        
        self.setup_views_and_controllers()
        self.setup_tabs()
        main_layout.addWidget(self.tab_widget)
        
        # Conecta la señal de cambio de pestaña para actualizar la lista de activos
        self.tab_widget.currentChanged.connect(self.handle_tab_change)

    def setup_views_and_controllers(self):
        # Creamos todas las vistas
        self.journal_view = JournalView()
        self.dashboard_view = DashboardView()
        self.maintenance_view = MaintenanceView()
        
        # Creamos los servicios
        self.analysis_service = AnalysisService(self.db_manager)
        self.maintenance_service = MaintenanceService(self.db_manager)

        # Creamos los controladores, pasándoles las dependencias
        self.journal_controller = JournalController(
            self.journal_view,
            self.db_manager,
            self.dashboard_view,
            self.analysis_service
        )
        self.maintenance_controller = MaintenanceController(
            self.maintenance_view,
            self.maintenance_service,
            self.user_id,
            self.journal_controller
        )

    def setup_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(self.journal_view, "Diario de Trading")
        self.tab_widget.addTab(self.dashboard_view, "Análisis")
        self.tab_widget.addTab(self.maintenance_view, "Mantenimiento")

        self.journal_controller.set_user_id(self.user_id)
        self.journal_controller.update_dashboard()

    def handle_tab_change(self, index):
        if self.tab_widget.tabText(index) == "Mantenimiento":
            self.maintenance_controller.load_assets()

def main():
    app = QApplication(sys.argv)
    
    # Este código no se ejecuta directamente, pero es útil para pruebas
    db_manager = DatabaseManager()
    main_window = MainWindow(user_id=1, db_manager=db_manager)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()