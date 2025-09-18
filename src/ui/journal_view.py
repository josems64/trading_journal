from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton,
    QComboBox, QDateEdit, QHBoxLayout, QLabel, QMessageBox, QDoubleSpinBox,
    QGroupBox, QTimeEdit, QGridLayout
)
from PyQt6.QtCore import QDate, QTime, Qt
from PyQt6.QtGui import QFont

class JournalView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        title_label = QLabel("Registro de Operación")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #4A90E2;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Contenedor principal de los bloques
        content_layout = QGridLayout()
        
        # Bloque de Datos Generales (Columna Izquierda)
        general_group = QGroupBox("Datos Generales")
        general_layout = QFormLayout(general_group)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        self.symbol_input = QComboBox()
        self.direction_input = QComboBox()
        self.direction_input.addItems(["", "Buy", "Sell"])

        general_layout.addRow("Fecha:", self.date_input)
        general_layout.addRow("Hora:", self.time_input)
        general_layout.addRow("Símbolo:", self.symbol_input)
        general_layout.addRow("Tendencia:", self.direction_input)
        content_layout.addWidget(general_group, 0, 0)

        # Bloque de Datos Financieros (Columna Derecha)
        financial_group = QGroupBox("Datos Financieros")
        financial_layout = QFormLayout(financial_group)
        self.entry_price_input = QLineEdit()
        self.stop_loss_input = QLineEdit()
        self.take_profit_input = QLineEdit()
        self.exit_price_input = QLineEdit()
        self.size_input = QLineEdit()
        self.profit_loss_usd_input = QLineEdit()
        self.risk_reward_input = QLineEdit()

        financial_layout.addRow("Precio de Entrada:", self.entry_price_input)
        financial_layout.addRow("Stop Loss:", self.stop_loss_input)
        financial_layout.addRow("Take Profit:", self.take_profit_input)
        financial_layout.addRow("Precio de Salida:", self.exit_price_input)
        financial_layout.addRow("Tamaño:", self.size_input)
        financial_layout.addRow("P&L (USD):", self.profit_loss_usd_input)
        financial_layout.addRow("R:R:", self.risk_reward_input)
        content_layout.addWidget(financial_group, 0, 1)

        # Bloque de Notas y Psicología (Debajo de los otros dos)
        psychological_group = QGroupBox("Notas y Psicología")
        psychological_layout = QFormLayout(psychological_group)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Describe el estado mental, emociones, etc.")
        self.strategy_input = QLineEdit()
        self.strategy_input.setPlaceholderText("Ej: Ruptura de soporte, Reversión en resistencia")

        psychological_layout.addRow("Estrategia:", self.strategy_input)
        psychological_layout.addRow("Notas:", self.notes_input)
        content_layout.addWidget(psychological_group, 1, 0, 1, 2)

        main_layout.addLayout(content_layout)

        # Botones de Acción
        self.save_button = QPushButton("Guardar Operación")
        self.clear_button = QPushButton("Limpiar Formulario")

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

    def get_form_data(self):
        return {
            'date': self.date_input.date().toString('yyyy-MM-dd'),
            'time': self.time_input.time().toString('HH:mm:ss'),
            'symbol': self.symbol_input.currentText(),
            'direction': self.direction_input.currentText(),
            'entry_price': self.entry_price_input.text(),
            'stop_loss': self.stop_loss_input.text(),
            'take_profit': self.take_profit_input.text(),
            'exit_price': self.exit_price_input.text(),
            'size': self.size_input.text(),
            'profit_loss_usd': self.profit_loss_usd_input.text(),
            'notes': self.notes_input.toPlainText(),
            'strategy': self.strategy_input.text(),
            'risk_reward': self.risk_reward_input.text(),
        }

    def clear_form(self):
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())
        self.symbol_input.setCurrentIndex(0)
        self.direction_input.setCurrentIndex(0)
        self.entry_price_input.clear()
        self.stop_loss_input.clear()
        self.take_profit_input.clear()
        self.exit_price_input.clear()
        self.size_input.clear()
        self.profit_loss_usd_input.clear()
        self.notes_input.clear()
        self.strategy_input.clear()
        self.risk_reward_input.clear()

    def set_symbols(self, symbols):
        self.symbol_input.clear()
        self.symbol_input.addItem("")
        self.symbol_input.addItems(symbols)