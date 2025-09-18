# Crea src/core/controllers/maintenance_controller.py

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QMessageBox
from src.ui.maintenance_view import MaintenanceView
from src.core.services.maintenance_service import MaintenanceService
from src.core.controllers.journal_controller import JournalController

class MaintenanceController(QObject):
    def __init__(self, view: MaintenanceView, service: MaintenanceService, user_id: int, journal_controller: JournalController):
        super().__init__()
        self.view = view
        self.service = service
        self.user_id = user_id
        self.journal_controller = journal_controller
        self.connect_signals()

    def connect_signals(self):
        self.view.add_asset_button.clicked.connect(self.add_asset)
        self.view.delete_asset_button.clicked.connect(self.delete_asset)

    def load_assets(self):
        assets = self.service.get_assets(self.user_id)
        self.view.update_asset_list(assets)

    def add_asset(self):
        asset_name = self.view.get_asset_name().upper().strip()
        if not asset_name:
            self.view.show_message("Error", "El nombre del activo no puede estar vacío.")
            return

        success, message = self.service.add_asset(self.user_id, asset_name)
        self.view.show_message("Agregar Activo", message)
        
        if success:
            self.load_assets()
            self.journal_controller.load_assets()
            self.view.asset_name_input.clear()

    def delete_asset(self):
        selected_asset = self.view.get_selected_asset()
        if not selected_asset:
            self.view.show_message("Error", "Por favor, selecciona un activo para eliminar.")
            return
        
        reply = QMessageBox.question(self.view, 'Eliminar Activo', f"¿Estás seguro de que deseas eliminar '{selected_asset}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.service.delete_asset(self.user_id, selected_asset)
            self.view.show_message("Eliminar Activo", message)
            if success:
                self.load_assets()
                self.journal_controller.load_assets()