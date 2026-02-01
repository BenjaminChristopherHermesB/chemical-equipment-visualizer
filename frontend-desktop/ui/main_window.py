from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget,
                             QPushButton, QFileDialog, QMessageBox, QMenuBar,
                             QMenu, QAction, QLabel, QInputDialog, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt
from api.client import APIClient
from ui.login_dialog import LoginDialog
from ui.data_table_widget import DataTableWidget
from ui.charts_widget import ChartsWidget
from ui.summary_widget import SummaryWidget
from ui.history_widget import HistoryWidget


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = None
        self.current_dataset = None
        self.user_data = None
        self.init_ui()
        self.show_login()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # User info label
        self.user_label = QLabel('Not logged in')
        self.user_label.setStyleSheet('font-weight: bold; padding: 5px;')
        main_layout.addWidget(self.user_label)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Upload tab
        upload_widget = QWidget()
        upload_layout = QVBoxLayout()
        
        upload_title = QLabel('Upload Chemical Equipment Data')
        upload_title.setStyleSheet('font-size: 18px; font-weight: bold; margin: 20px;')
        upload_layout.addWidget(upload_title)
        
        upload_desc = QLabel('Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature')
        upload_desc.setStyleSheet('color: gray; margin: 10px;')
        upload_desc.setWordWrap(True)
        upload_layout.addWidget(upload_desc)
        
        upload_btn = QPushButton('Choose CSV File')
        upload_btn.clicked.connect(self.handle_upload)
        upload_btn.setStyleSheet('padding: 10px; font-size: 14px;')
        upload_layout.addWidget(upload_btn)
        
        upload_layout.addStretch()
        upload_widget.setLayout(upload_layout)
        
        # Visualization tab
        viz_tab = QWidget()
        viz_tab_layout = QVBoxLayout(viz_tab)
        viz_tab_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for visualization
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        viz_widget = QWidget()
        viz_layout = QVBoxLayout()
        viz_layout.setSpacing(20)  # Add spacing between elements
        viz_widget.setLayout(viz_layout)
        
        scroll_area.setWidget(viz_widget)
        viz_tab_layout.addWidget(scroll_area)
        
        # Dataset header
        header_layout = QHBoxLayout()
        self.dataset_label = QLabel('No dataset loaded')
        self.dataset_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        header_layout.addWidget(self.dataset_label)
        header_layout.addStretch()
        
        self.pdf_btn = QPushButton('Download PDF Report')
        self.pdf_btn.clicked.connect(self.handle_download_pdf)
        self.pdf_btn.setEnabled(False)
        header_layout.addWidget(self.pdf_btn)
        
        viz_layout.addLayout(header_layout)
        
        # Summary widget
        self.summary_widget = SummaryWidget()
        viz_layout.addWidget(self.summary_widget)
        
        # Data table
        self.data_table = DataTableWidget()
        self.data_table.setMinimumHeight(400)  # Ensure table has enough height
        viz_layout.addWidget(self.data_table)
        
        # Charts
        self.charts_widget = ChartsWidget()
        self.charts_widget.setMinimumHeight(800)  # Ensure charts have enough room
        viz_layout.addWidget(self.charts_widget)
        
        # History tab
        self.history_widget = HistoryWidget(None)
        self.history_widget.dataset_selected.connect(self.load_dataset)
        
        # Add tabs
        self.tabs.addTab(upload_widget, 'Upload CSV')
        self.tabs.addTab(viz_tab, 'Visualization')
        self.tabs.addTab(self.history_widget, 'History')
        
        main_layout.addWidget(self.tabs)
        
        # Menu bar
        self.create_menu_bar()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        upload_action = QAction('Upload CSV', self)
        upload_action.triggered.connect(self.handle_upload)
        file_menu.addAction(upload_action)
        
        file_menu.addSeparator()
        
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.handle_logout)
        file_menu.addAction(logout_action)
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu('Settings')
        
        api_url_action = QAction('Set API URL', self)
        api_url_action.triggered.connect(self.set_api_url)
        settings_menu.addAction(api_url_action)
    
    def show_login(self):
        """Show login dialog"""
        # Use default production URL defined in APIClient
        self.api_client = APIClient()
        self.history_widget.api_client = self.api_client
        
        login_dialog = LoginDialog(self.api_client, self)
        if login_dialog.exec_() == LoginDialog.Accepted:
            self.user_data = login_dialog.user_data
            self.user_label.setText(f"Logged in as: {self.user_data['username']}")
            self.history_widget.load_history()
        else:
            self.close()
    
    def set_api_url(self):
        """Change API URL"""
        current_url = self.api_client.base_url if self.api_client else 'http://localhost:8000/api'
        new_url, ok = QInputDialog.getText(self, 'API URL', 
                                          'Enter new API Base URL:',
                                          text=current_url)
        if ok and new_url:
            if self.api_client:
                self.api_client.base_url = new_url.rstrip('/')
                QMessageBox.information(self, 'Success', 'API URL updated')
    
    def handle_upload(self):
        """Handle CSV upload"""
        if not self.api_client or not self.api_client.token:
            QMessageBox.warning(self, 'Error', 'Please login first')
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 
                                                   'CSV Files (*.csv)')
        if not file_path:
            return
        
        try:
            result = self.api_client.upload_csv(file_path)
            dataset = result['dataset']
            QMessageBox.information(self, 'Success', 'CSV uploaded successfully!')
            self.load_dataset(dataset)
            self.tabs.setCurrentIndex(1)  # Switch to visualization tab
            self.history_widget.load_history()  # Refresh history
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload failed: {str(e)}')
    
    def load_dataset(self, dataset):
        """Load dataset into visualization"""
        self.current_dataset = dataset
        self.dataset_label.setText(f"Dataset: {dataset.get('filename', 'Unknown')}")
        self.pdf_btn.setEnabled(True)
        
        # Load data
        raw_data = dataset.get('raw_data', [])
        summary_stats = dataset.get('summary_stats', {})
        row_count = dataset.get('row_count', 0)
        
        self.summary_widget.load_stats(summary_stats, row_count)
        self.data_table.load_data(raw_data)
        self.charts_widget.load_data(raw_data, summary_stats)
    
    def handle_download_pdf(self):
        """Download PDF report"""
        if not self.current_dataset:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save PDF Report', 
                                                   f"{self.current_dataset.get('filename', 'report')}.pdf",
                                                   'PDF Files (*.pdf)')
        if not file_path:
            return
        
        try:
            self.api_client.download_pdf(self.current_dataset['id'], file_path)
            QMessageBox.information(self, 'Success', f'PDF saved to {file_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'PDF download failed: {str(e)}')
    
    def handle_logout(self):
        """Logout and show login dialog"""
        if self.api_client:
            self.api_client.logout()
        
        self.current_dataset = None
        self.dataset_label.setText('No dataset loaded')
        self.pdf_btn.setEnabled(False)
        self.data_table.setRowCount(0)
        
        self.show_login()
