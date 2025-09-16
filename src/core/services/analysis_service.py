import sqlite3
from ..database import DatabaseManager

class AnalysisService:
    """
    Servicio que gestiona la lógica de análisis de datos del diario de trading.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_key_metrics(self):
        """
        Calcula y retorna las métricas clave de la bitácora.
        """
        all_trades = self._get_all_trades_data()
        
        if not all_trades:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'total_profit': 0.0
            }

        total_trades = len(all_trades)
        winning_trades = [trade for trade in all_trades if trade['trade_outcome'] == 'Win']
        total_profit = sum(trade['profit_loss_usd'] for trade in all_trades)
        
        win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'total_profit': total_profit
        }

    def _get_all_trades_data(self):
        """
        Obtiene todos los registros de trades de la base de datos como diccionarios.
        """
        self.db_manager.connect()
        if self.db_manager.conn is None:
            return []
        
        try:
            cursor = self.db_manager.cursor
            # Usar PRAGMA table_info para obtener los nombres de las columnas
            cursor.execute("PRAGMA table_info(trades)")
            columns = [col[1] for col in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM trades")
            rows = cursor.fetchall()
            
            # Convertir las filas a diccionarios
            trades_list = [dict(zip(columns, row)) for row in rows]
            return trades_list
        except sqlite3.Error as e:
            print(f"Error al obtener los datos: {e}")
            return []
        finally:
            self.db_manager.disconnect()