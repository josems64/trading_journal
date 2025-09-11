from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from src.core.database import DatabaseManager # Importar el gestor de la DB
from src.core.controllers.journal_controller import JournalController # Importar el nuevo controlador
from src.ui.journal_view import JournalView
from src.ui.graph_widget import GraphWidget
from src.ui.risk_manager_widget import RiskManagerWidget
from src.ui.portfolio_widget import PortfolioWidget
from src.ui.maintenance_widget import MaintenanceWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Journal App")
        self.setGeometry(100, 100, 1200, 800)

        self.db_manager = DatabaseManager() # Instanciar la base de datos

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.setup_tabs()

    def setup_tabs(self):
        # Pestaña de Registro de Operaciones
        journal_tab = JournalView()
        # Instanciar el controlador y pasarle la vista y el gestor de la DB
        self.journal_controller = JournalController(journal_tab, self.db_manager) 
        self.tab_widget.addTab(journal_tab, "Registro de Operaciones")

        # ... (el resto del código de setup_tabs es el mismo)
        graphs_tab = GraphWidget()
        self.tab_widget.addTab(graphs_tab, "Gráficos")

        risk_manager_tab = RiskManagerWidget()
        self.tab_widget.addTab(risk_manager_tab, "Gestión de Riesgos")

        portfolio_tab = PortfolioWidget()
        self.tab_widget.addTab(portfolio_tab, "Portafolio")

        maintenance_tab = MaintenanceWidget()
        self.tab_widget.addTab(maintenance_tab, "Mantenimiento")