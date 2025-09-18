# Abre src/ui/maintenance_view.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont

class MaintenanceView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        title_label = QLabel("Mantenimiento de Activos")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #4A90E2;")
        main_layout.addWidget(title_label)
        
        # Formulario para agregar activo
        asset_form_layout = QFormLayout()
        self.asset_name_input = QLineEdit()
        self.add_asset_button = QPushButton("Agregar")
        
        asset_form_layout.addRow("Nombre del Activo:", self.asset_name_input)
        asset_form_layout.addRow("", self.add_asset_button)
        
        main_layout.addLayout(asset_form_layout)
        
        # Lista de activos
        asset_list_label = QLabel("Activos Existentes:")
        font.setPointSize(12)
        font.setBold(False)
        asset_list_label.setFont(font)
        main_layout.addWidget(asset_list_label)
        
        self.asset_list_widget = QListWidget()
        main_layout.addWidget(self.asset_list_widget)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        self.delete_asset_button = QPushButton("Eliminar")
        buttons_layout.addWidget(self.delete_asset_button)
        
        main_layout.addLayout(buttons_layout)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def get_asset_name(self):
        return self.asset_name_input.text()

    def get_selected_asset(self):
        selected_items = self.asset_list_widget.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

    def update_asset_list(self, assets):
        self.asset_list_widget.clear()
        for asset in assets:
            self.asset_list_widget.addItem(asset)