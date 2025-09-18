# Abre src/core/services/maintenance_service.py

from src.core.database import DatabaseManager
import sqlite3

class MaintenanceService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add_asset(self, user_id, asset_name):
        """Agrega un nuevo activo a la base de datos."""
        self.db_manager.connect()
        try:
            self.db_manager.cursor.execute(
                "INSERT INTO assets (user_id, name) VALUES (?, ?)",
                (user_id, asset_name)
            )
            self.db_manager.conn.commit()
            return True, f"Activo '{asset_name}' agregado exitosamente."
        except sqlite3.IntegrityError:
            return False, f"El activo '{asset_name}' ya existe."
        except sqlite3.Error as e:
            return False, f"Error al agregar el activo: {e}"
        finally:
            self.db_manager.disconnect()

    def delete_asset(self, user_id, asset_name):
        """Elimina un activo de la base de datos."""
        self.db_manager.connect()
        try:
            self.db_manager.cursor.execute(
                "DELETE FROM assets WHERE user_id = ? AND name = ?",
                (user_id, asset_name)
            )
            self.db_manager.conn.commit()
            return True, f"Activo '{asset_name}' eliminado exitosamente."
        except sqlite3.Error as e:
            return False, f"Error al eliminar el activo: {e}"
        finally:
            self.db_manager.disconnect()

    def get_assets(self, user_id):
        """Obtiene todos los activos registrados por un usuario."""
        self.db_manager.connect()
        try:
            self.db_manager.cursor.execute(
                "SELECT name FROM assets WHERE user_id = ?",
                (user_id,)
            )
            assets = [row[0] for row in self.db_manager.cursor.fetchall()]
            return assets
        except sqlite3.Error as e:
            return []
        finally:
            self.db_manager.disconnect()