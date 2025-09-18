import sqlite3
from src.core.database import DatabaseManager

class AnalysisService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_total_trades(self, user_id):
        """Retorna el número total de operaciones de un usuario."""
        self.db_manager.connect()
        try:
            self.db_manager.cursor.execute(
                "SELECT COUNT(*) FROM trades WHERE user_id = ?",
                (user_id,)
            )
            total_trades = self.db_manager.cursor.fetchone()[0]
            return total_trades
        except sqlite3.Error as e:
            print(f"Error al obtener el total de operaciones: {e}")
            return 0
        finally:
            self.db_manager.disconnect()

    def get_win_rate(self, user_id):
        """Calcula el porcentaje de operaciones ganadoras de un usuario."""
        self.db_manager.connect()
        try:
            self.db_manager.cursor.execute(
                "SELECT COUNT(*) FROM trades WHERE user_id = ? AND trade_outcome = 'Win'",
                (user_id,)
            )
            total_wins = self.db_manager.cursor.fetchone()[0]
            
            self.db_manager.cursor.execute(
                "SELECT COUNT(*) FROM trades WHERE user_id = ? AND trade_outcome IN ('Win', 'Loss')",
                (user_id,)
            )
            total_resolved_trades = self.db_manager.cursor.fetchone()[0]
            
            if total_resolved_trades == 0:
                return 0.0
            
            win_rate = (total_wins / total_resolved_trades) * 100
            return win_rate
        except sqlite3.Error as e:
            print(f"Error al calcular el porcentaje de victorias: {e}")
            return 0.0
        finally:
            self.db_manager.disconnect()

    def get_total_profit(self, user_id):
        """Calcula la ganancia o pérdida total de un usuario en USD."""
        self.db_manager.connect()
        try:
            self.db_manager.cursor.execute(
                "SELECT SUM(profit_loss_usd) FROM trades WHERE user_id = ?",
                (user_id,)
            )
            total_profit = self.db_manager.cursor.fetchone()[0]
            if total_profit is None:
                return 0.0
            return total_profit
        except sqlite3.Error as e:
            print(f"Error al calcular la ganancia total: {e}")
            return 0.0
        finally:
            self.db_manager.disconnect()