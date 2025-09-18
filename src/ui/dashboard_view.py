from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        title_label = QLabel("Análisis de Operaciones")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #4A90E2;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Labels para mostrar las estadísticas
        self.total_trades_label = QLabel("Total de operaciones: 0")
        self.win_rate_label = QLabel("Tasa de victorias: 0.00%")
        self.total_profit_label = QLabel("Ganancia total: $0.00")
        
        font.setPointSize(12)
        font.setBold(False)
        self.total_trades_label.setFont(font)
        self.win_rate_label.setFont(font)
        self.total_profit_label.setFont(font)
        
        main_layout.addWidget(self.total_trades_label)
        main_layout.addWidget(self.win_rate_label)
        main_layout.addWidget(self.total_profit_label)
        
        main_layout.addStretch()

    def update_stats(self, stats):
        """
        Actualiza los labels con las estadísticas recibidas.
        """
        self.total_trades_label.setText(f"Total de operaciones: {stats['total_trades']}")
        self.win_rate_label.setText(f"Tasa de victorias: {stats['win_rate']}")
        self.total_profit_label.setText(f"Ganancia total: ${stats['total_profit']}")