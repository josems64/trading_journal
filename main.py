import sys
from PyQt6.QtWidgets import QApplication
from src.core.database import DatabaseManager
from src.ui.main_window import MainWindow
from src.ui.journal_view import JournalView
from src.core.controllers.journal_controller import JournalController
from src.ui.journal_view import JournalView
from src.ui.dashboard_view import DashboardView
from src.core.services.analysis_service import AnalysisService

def main():

    app = QApplication(sys.argv)

    db_manager = DatabaseManager()
    analysis_service = AnalysisService(db_manager)
    
    # Creamos las vistas
    journal_view = JournalView()
    dashboard_view = DashboardView()
    
    # Pasamos todas las dependencias necesarias al controlador
    journal_controller = JournalController(
        journal_view,
        db_manager,
        dashboard_view,
        analysis_service
    )

    main_window = MainWindow(journal_view, dashboard_view, journal_controller)
    main_window.show()
    
    sys.exit(app.exec())

    """
    Función principal que inicializa y ejecuta la aplicación.
    """
    # 1. Instanciar el modelo (DatabaseManager)
    db_manager = DatabaseManager()

    # 2. Instanciar la vista principal y sus componentes
    app = QApplication(sys.argv)
    main_window = MainWindow()
    
    # 3. Obtener la instancia de la vista de registro (ya creada en MainWindow)
    journal_view = main_window.findChild(JournalView)
    
    # 4. Instanciar el controlador y conectar la vista con el modelo
    if journal_view:
        journal_controller = JournalController(journal_view, db_manager)
    
    # 5. Mostrar la ventana principal
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()