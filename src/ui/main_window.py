from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
# Importar los widgets que acabas de crear
from src.ui.journal_view import JournalView
from src.ui.graph_widget import GraphWidget
from src.ui.risk_manager_widget import RiskManagerWidget
from src.ui.portfolio_widget import PortfolioWidget
from src.ui.maintenance_widget import MaintenanceWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Journal App")
        self.setGeometry(100, 100, 1200, 800)  # Aumentamos el tamaño

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.setup_tabs()

    def setup_tabs(self):
        """
        Configura y añade las pestañas a la ventana principal.
        """
        # Registro de Operaciones
        journal_tab = JournalView()
        self.tab_widget.addTab(journal_tab, "Registro de Operaciones")

        # Gráficos (ahora con el widget)
        graphs_tab = GraphWidget()
        self.tab_widget.addTab(graphs_tab, "Gráficos")

        # Gestión de Riesgos (ahora con el widget)
        risk_manager_tab = RiskManagerWidget()
        self.tab_widget.addTab(risk_manager_tab, "Gestión de Riesgos")

        # Portafolio (ahora con el widget)
        portfolio_tab = PortfolioWidget()
        self.tab_widget.addTab(portfolio_tab, "Portafolio")

        # Mantenimiento (ahora con el widget)
        maintenance_tab = MaintenanceWidget()
        self.tab_widget.addTab(maintenance_tab, "Mantenimiento")