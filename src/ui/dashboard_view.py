from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel
from PyQt6.QtGui import QFont

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Título de la sección
        title_label = QLabel("Dashboard de Análisis")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #4A90E2;")
        main_layout.addWidget(title_label)

        # Espacio para las métricas clave
        metrics_group = QGroupBox("Métricas Clave de Rendimiento")
        metrics_layout = QFormLayout()

        self.total_trades_label = QLabel("Total de Operaciones: 0")
        self.win_rate_label = QLabel("Ratio de Ganancia: 0%")
        self.total_profit_label = QLabel("Ganancia Neta: $0.00")

        metrics_layout.addRow(self.total_trades_label)
        metrics_layout.addRow(self.win_rate_label)
        metrics_layout.addRow(self.total_profit_label)

        metrics_group.setLayout(metrics_layout)
        main_layout.addWidget(metrics_group)
        main_layout.addStretch()

    def update_metrics(self, metrics):
        """
        Actualiza las etiquetas con los valores de las métricas.
        """
        self.total_trades_label.setText(f"Total de Operaciones: {metrics['total_trades']}")
        self.win_rate_label.setText(f"Ratio de Ganancia: {metrics['win_rate']:.2f}%")
        self.total_profit_label.setText(f"Ganancia Neta: ${metrics['total_profit']:.2f}")
