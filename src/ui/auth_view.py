from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel,
    QMessageBox, QStackedWidget,QApplication,QHBoxLayout
)
from PyQt6.QtGui import QFont

class AuthView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Autenticación")
        self.setGeometry(100, 100, 400, 250)

        self.stacked_widget = QStackedWidget(self)
        self.login_widget = QWidget()
        self.register_widget = QWidget()

        self.setup_login_ui()
        self.setup_register_ui()

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        self.setFont(QFont("Arial", 12))

        # Obtenemos la geometria de la pantalla principal
        screen_geometry = QApplication.primaryScreen().geometry()
        # Calculamos la posición para centrar la ventana
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        # Movemos la ventana a la posición calculada
        self.move(int(x), int(y))

    def setup_login_ui(self):
        layout = QVBoxLayout(self.login_widget)
        form_layout = QFormLayout()

        self.login_username_input = QLineEdit()
    
        password_layout = QHBoxLayout()
        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password_toggle = QPushButton("👁️")
        self.login_password_toggle.setFixedSize(30, 30)
        self.login_password_toggle.setCheckable(True)
        password_layout.addWidget(self.login_password_input)
        password_layout.addWidget(self.login_password_toggle)

        form_layout.addRow("Usuario:", self.login_username_input)
        form_layout.addRow("Contraseña:", password_layout)

        self.login_password_toggle.clicked.connect(self.toggle_login_password_visibility)

        self.login_button = QPushButton("Iniciar Sesión")
        self.go_to_register_button = QPushButton("Registrarse")

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        layout.addWidget(self.go_to_register_button)
        layout.addStretch()

    def setup_register_ui(self):
        layout = QVBoxLayout(self.register_widget)
        form_layout = QFormLayout()

        self.register_username_input = QLineEdit()
    
        # Contraseña
        register_password_layout = QHBoxLayout()
        self.register_password_input = QLineEdit()
        self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password_toggle = QPushButton("👁️")
        self.register_password_toggle.setFixedSize(30, 30)
        self.register_password_toggle.setCheckable(True)
        register_password_layout.addWidget(self.register_password_input)
        register_password_layout.addWidget(self.register_password_toggle)

        # Confirmar Contraseña
        register_confirm_password_layout = QHBoxLayout()
        self.register_confirm_password_input = QLineEdit()
        self.register_confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_confirm_password_toggle = QPushButton("👁️")
        self.register_confirm_password_toggle.setFixedSize(30, 30)
        self.register_confirm_password_toggle.setCheckable(True)
        register_confirm_password_layout.addWidget(self.register_confirm_password_input)
        register_confirm_password_layout.addWidget(self.register_confirm_password_toggle)
    
        self.register_first_name_input = QLineEdit()
        self.register_last_name_input = QLineEdit()
        self.register_email_input = QLineEdit()

        form_layout.addRow("Usuario:", self.register_username_input)
        form_layout.addRow("Contraseña:", register_password_layout)
        form_layout.addRow("Confirmar Contraseña:", register_confirm_password_layout)
        form_layout.addRow("Nombre:", self.register_first_name_input)
        form_layout.addRow("Apellido:", self.register_last_name_input)
        form_layout.addRow("Correo:", self.register_email_input)

        self.register_password_toggle.clicked.connect(self.toggle_register_password_visibility)
        self.register_confirm_password_toggle.clicked.connect(self.toggle_register_confirm_password_visibility)

        self.register_button = QPushButton("Registrar")
        self.go_to_login_button = QPushButton("Volver a Iniciar Sesión")

        layout.addLayout(form_layout)
        layout.addWidget(self.register_button)
        layout.addWidget(self.go_to_login_button)
        layout.addStretch()

    def toggle_login_password_visibility(self, checked):
        if checked:
            self.login_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.login_password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_register_password_visibility(self, checked):
        if checked:
            self.register_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_register_confirm_password_visibility(self, checked):
        if checked:
            self.register_confirm_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.register_confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)
        self.setWindowTitle("Iniciar Sesión")

    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register_widget)
        self.setWindowTitle("Registrarse")

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

    def get_login_data(self):
        return self.login_username_input.text(), self.login_password_input.text()

    def get_register_data(self):
        return (
        self.register_username_input.text(),
        self.register_password_input.text(),
        self.register_confirm_password_input.text(),
        self.register_first_name_input.text(),
        self.register_last_name_input.text(),
        self.register_email_input.text()
        )