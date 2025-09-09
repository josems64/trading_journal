from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PortfolioWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Aquí gestionarás tu portafolio.")
        layout.addWidget(label)