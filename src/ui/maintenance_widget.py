from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class MaintenanceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Esta es la sección de mantenimiento de la base de datos.")
        layout.addWidget(label)