from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, 
    QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QComboBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QDate

class JournalView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Establecer la fuente base para toda la vista
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        
        main_layout = QVBoxLayout(self)

        # 1. Grupo para los datos básicos
        basic_group = QGroupBox("Datos Principales de la Operación")
        basic_layout = QFormLayout()
        
        self.date_input = QLineEdit()
        self.date_input.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        self.date_input.setPlaceholderText("Ej: 13/09/2025")

        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Ej: BTC/USD")
        
        self.direction_input = QComboBox()
        self.direction_input.addItem("Buy")
        self.direction_input.addItem("Sell")
        
        basic_layout.addRow("Fecha:", self.date_input)
        basic_layout.addRow("Símbolo:", self.symbol_input)
        basic_layout.addRow("Dirección:", self.direction_input)
        basic_group.setLayout(basic_layout)

        # 2. Grupo para precios y tamaño
        price_group = QGroupBox("Precios y Cantidad")
        price_layout = QFormLayout()
        
        self.entry_price_input = QLineEdit()
        self.entry_price_input.setPlaceholderText("Ej: 20000.00")
        
        self.stop_loss_input = QLineEdit()
        self.stop_loss_input.setPlaceholderText("Ej: 19800.00")
        
        self.take_profit_input = QLineEdit()
        self.take_profit_input.setPlaceholderText("Ej: 21000.00")
        
        self.exit_price_input = QLineEdit()
        self.exit_price_input.setPlaceholderText("Ej: 20500.00")
        
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Tamaño de Lote Ej: 0.1 o 0.01")
        
        price_layout.addRow("Precio de Entrada:", self.entry_price_input)
        price_layout.addRow("Stop Loss:", self.stop_loss_input)
        price_layout.addRow("Take Profit:", self.take_profit_input)
        price_layout.addRow("Precio de Salida:", self.exit_price_input)
        price_layout.addRow("Tamaño:", self.size_input)
        price_group.setLayout(price_layout)

        # 3. Grupo para notas y el botón
        notes_group = QGroupBox("Notas y Acción")
        notes_layout = QFormLayout()
        
        self.strategy_input = QLineEdit()
        self.strategy_input.setPlaceholderText("Ej: Scalping")
        
        self.risk_reward_input = QLineEdit()
        self.risk_reward_input.setPlaceholderText("Ej: 2.5")
        
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Ej: El mercado estaba muy volátil.")

        self.save_button = QPushButton("Guardar Operación")
        
        notes_layout.addRow("Estrategia:", self.strategy_input)
        notes_layout.addRow("Riesgo/Recompensa (RR):", self.risk_reward_input)
        notes_layout.addRow("Notas:", self.notes_input)
        notes_layout.addWidget(self.save_button)
        notes_group.setLayout(notes_layout)

        # Agrupar los elementos en un layout horizontal para mayor profesionalismo
        top_layout = QHBoxLayout()
        top_layout.addWidget(basic_group)
        top_layout.addWidget(price_group)

        # Añadir todos los grupos al layout principal
        main_layout.addLayout(top_layout)
        main_layout.addWidget(notes_group)
        main_layout.addStretch()

   