import sys
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QApplication
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self, journal_view, dashboard_view, journal_controller):
        super().__init__()
        self.setWindowTitle("Trading Journal Pro")
        self.setGeometry(100, 100, 800, 600)

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        
        self.journal_view = journal_view
        self.dashboard_view = dashboard_view
        self.journal_controller = journal_controller

        self.setup_tabs()

    def setup_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
        self.tab_widget.addTab(self.journal_view, "Diario de Trading")
        self.tab_widget.addTab(self.dashboard_view, "Análisis")

        self.journal_controller.update_dashboard()

def main():
    app = QApplication(sys.argv)
    
    # Importaciones aquí para evitar errores circulares
    from src.core.database import DatabaseManager
    from src.core.controllers.journal_controller import JournalController
    from src.core.services.analysis_service import AnalysisService
    from src.ui.journal_view import JournalView
    from src.ui.dashboard_view import DashboardView

    db_manager = DatabaseManager()
    analysis_service = AnalysisService(db_manager)
    
    journal_view = JournalView()
    dashboard_view = DashboardView()
    
    journal_controller = JournalController(
        journal_view,
        db_manager,
        dashboard_view,
        analysis_service
    )

    main_window = MainWindow(journal_view, dashboard_view, journal_controller)
    main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()