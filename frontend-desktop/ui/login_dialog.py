from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QTabWidget, QWidget)
from PyQt5.QtCore import Qt
from api.client import APIClient


class LoginDialog(QDialog):
    """Login/Register Dialog"""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Chemical Equipment Visualizer')
        title.setStyleSheet('font-size: 20px; font-weight: bold; margin: 10px;')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tabs for Login/Register
        self.tabs = QTabWidget()
        
        # Login Tab
        login_tab = QWidget()
        login_layout = QVBoxLayout()
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('Username')
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Password')
        self.login_password.setEchoMode(QLineEdit.Password)
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.handle_login)
        
        login_layout.addWidget(QLabel('Username:'))
        login_layout.addWidget(self.login_username)
        login_layout.addWidget(QLabel('Password:'))
        login_layout.addWidget(self.login_password)
        login_layout.addWidget(login_btn)
        login_layout.addStretch()
        
        login_tab.setLayout(login_layout)
        
        # Register Tab
        register_tab = QWidget()
        register_layout = QVBoxLayout()
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText('Username')
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText('Email (optional)')
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText('Password')
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password2 = QLineEdit()
        self.register_password2.setPlaceholderText('Confirm Password')
        self.register_password2.setEchoMode(QLineEdit.Password)
        
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.handle_register)
        
        register_layout.addWidget(QLabel('Username:'))
        register_layout.addWidget(self.register_username)
        register_layout.addWidget(QLabel('Email (optional):'))
        register_layout.addWidget(self.register_email)
        register_layout.addWidget(QLabel('Password:'))
        register_layout.addWidget(self.register_password)
        register_layout.addWidget(QLabel('Confirm Password:'))
        register_layout.addWidget(self.register_password2)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        
        register_tab.setLayout(register_layout)
        
        self.tabs.addTab(login_tab, 'Login')
        self.tabs.addTab(register_tab, 'Register')
        
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            result = self.api_client.login(username, password)
            self.user_data = result['user']
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def handle_register(self):
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        password2 = self.register_password2.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        if password != password2:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return
        
        try:
            result = self.api_client.register(username, email, password, password2)
            self.user_data = result['user']
            QMessageBox.information(self, 'Success', 'Registration successful!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
