from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, 
    QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout
)

class JournalView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # 1. Grupo para los datos básicos de la operación
        basic_group = QGroupBox("Datos Principales de la Operación")
        basic_layout = QFormLayout()
        
        self.date_input = QLineEdit()
        self.symbol_input = QLineEdit()
        self.direction_input = QLineEdit()
        
        basic_layout.addRow("Fecha:", self.date_input)
        basic_layout.addRow("Símbolo:", self.symbol_input)
        basic_layout.addRow("Dirección:", self.direction_input)
        basic_group.setLayout(basic_layout)

        # 2. Grupo para los datos de precios y tamaño
        price_group = QGroupBox("Precios y Cantidad")
        price_layout = QFormLayout()
        
        self.entry_price_input = QLineEdit()
        self.stop_loss_input = QLineEdit() # Nuevo campo: Stop Loss
        self.take_profit_input = QLineEdit() # Nuevo campo: Take Profit
        self.exit_price_input = QLineEdit()
        self.size_input = QLineEdit()
        
        price_layout.addRow("Precio de Entrada:", self.entry_price_input)
        price_layout.addRow("Stop Loss:", self.stop_loss_input)
        price_layout.addRow("Take Profit:", self.take_profit_input)
        price_layout.addRow("Precio de Salida:", self.exit_price_input)
        price_layout.addRow("Tamaño:", self.size_input)
        price_group.setLayout(price_layout)

        # 3. Grupo para datos adicionales y el botón
        notes_group = QGroupBox("Notas y Acción")
        notes_layout = QVBoxLayout()
        
        self.strategy_input = QLineEdit() # Nuevo campo: Estrategia
        self.risk_reward_input = QLineEdit() # Nuevo campo: Riesgo/Recompensa
        self.notes_input = QLineEdit()
        self.save_button = QPushButton("Guardar Operación")
        
        notes_layout.addWidget(QLabel("Estrategia:"))
        notes_layout.addWidget(self.strategy_input)
        notes_layout.addWidget(QLabel("Riesgo/Recompensa (RR):"))
        notes_layout.addWidget(self.risk_reward_input)
        notes_layout.addWidget(QLabel("Notas:"))
        notes_layout.addWidget(self.notes_input)
        notes_layout.addWidget(self.save_button)
        notes_group.setLayout(notes_layout)

        # 4. Agrupar los elementos
        top_layout = QHBoxLayout()
        top_layout.addWidget(basic_group)
        top_layout.addWidget(price_group)

        # 5. Añadir todos los grupos al layout principal
        main_layout.addLayout(top_layout)
        main_layout.addWidget(notes_group)
        main_layout.addStretch()