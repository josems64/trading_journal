import sys
from PyQt6.QtWidgets import QApplication
from src.core.database import DatabaseManager
from src.ui.main_window import MainWindow
from src.ui.auth_view import AuthView
from src.core.services.auth_service import AuthService

class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.db_manager = DatabaseManager()
        self.auth_service = AuthService(self.db_manager)

        self.auth_view = AuthView()
        self.auth_view.login_button.clicked.connect(self.handle_login)
        self.auth_view.register_button.clicked.connect(self.handle_register)
        self.auth_view.go_to_register_button.clicked.connect(self.auth_view.show_register)
        self.auth_view.go_to_login_button.clicked.connect(self.auth_view.show_login)

        self.auth_view.show()
        self.user_id = None
        self.main_window = None

    def handle_login(self):
        username, password = self.auth_view.get_login_data()
        user_id, message = self.auth_service.login_user(username, password)
        if user_id:
            self.user_id = user_id
            self.show_main_window()
            self.auth_view.close()
        else:
            self.auth_view.show_message("Error de inicio de sesión", message)

    def handle_register(self):
        username, password, confirm_password, first_name, last_name, email = self.auth_view.get_register_data()
        if password != confirm_password:
            self.auth_view.show_message("Error", "Las contraseñas no coinciden.")
            return

        success, message = self.auth_service.register_user(username, password, first_name, last_name, email)
        if success:
            self.auth_view.show_message("Registro Exitoso", message)
            self.auth_view.show_login()
        else:
            self.auth_view.show_message("Error de Registro", message)

    def show_main_window(self):
        self.main_window = MainWindow(self.user_id, self.db_manager)
        self.main_window.show()

def main():
    app = App(sys.argv)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()