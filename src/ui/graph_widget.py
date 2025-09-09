from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Aquí irán los gráficos y el análisis.")
        layout.addWidget(label)