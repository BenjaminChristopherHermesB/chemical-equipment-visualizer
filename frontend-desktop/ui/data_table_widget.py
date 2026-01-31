from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt


class DataTableWidget(QTableWidget):
    """Table widget for displaying equipment data"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def load_data(self, data):
        """Load data into the table"""
        if not data:
            return
        
        columns = list(data[0].keys())
        self.setColumnCount(len(columns))
        self.setRowCount(len(data))
        self.setHorizontalHeaderLabels(columns)
        
        for row_idx, row_data in enumerate(data):
            for col_idx, column in enumerate(columns):
                value = row_data.get(column, '-')
                if value is None:
                    value = '-'
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.setItem(row_idx, col_idx, item)
