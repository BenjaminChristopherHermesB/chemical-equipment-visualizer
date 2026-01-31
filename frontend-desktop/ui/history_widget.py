from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, 
                             QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from api.client import APIClient


class HistoryWidget(QWidget):
    """Widget for displaying dataset history"""
    
    dataset_selected = pyqtSignal(dict)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('Recent Uploads (Last 5)')
        title.setStyleSheet('font-size: 16px; font-weight: bold; margin: 10px;')
        layout.addWidget(title)
        
        subtitle = QLabel('Double-click on any dataset to view details')
        subtitle.setStyleSheet('color: gray; margin-bottom: 10px;')
        layout.addWidget(subtitle)
        
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        self.setLayout(layout)
    
    def load_history(self):
        """Load dataset history"""
        try:
            result = self.api_client.get_datasets()
            datasets = result.get('results', [])
            
            self.list_widget.clear()
            for dataset in datasets:
                item_text = f"{dataset['filename']} - {dataset['uploaded_at']} ({dataset['row_count']} records)"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, dataset)
                self.list_widget.addItem(item)
            
            if not datasets:
                item = QListWidgetItem('No datasets uploaded yet')
                item.setFlags(Qt.NoItemFlags)
                self.list_widget.addItem(item)
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load history: {str(e)}')
    
    def on_item_double_clicked(self, item):
        """Handle item double-click"""
        dataset = item.data(Qt.UserRole)
        if dataset:
            try:
                full_dataset = self.api_client.get_dataset(dataset['id'])
                self.dataset_selected.emit(full_dataset)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
