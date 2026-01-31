from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt


class SummaryWidget(QWidget):
    """Widget for displaying summary statistics"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('Summary Statistics')
        title.setStyleSheet('font-size: 16px; font-weight: bold; margin: 10px;')
        layout.addWidget(title)
        
        self.stats_layout = QGridLayout()
        layout.addLayout(self.stats_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def load_stats(self, stats, row_count):
        """Load and display statistics"""
        # Clear previous stats
        for i in reversed(range(self.stats_layout.count())): 
            self.stats_layout.itemAt(i).widget().setParent(None)
        
        if not stats:
            return
        
        # Total Count
        total_label = QLabel(f"<b>Total Records:</b> {stats.get('total_count', row_count)}")
        self.stats_layout.addWidget(total_label, 0, 0, 1, 2)
        
        # Flowrate Stats
        flowrate_title = QLabel("<b>Flowrate Statistics</b>")
        self.stats_layout.addWidget(flowrate_title, 1, 0)
        
        flowrate = stats.get('flowrate', {})
        flowrate_text = f"""
        Mean: {flowrate.get('mean', 0)}
        Min: {flowrate.get('min', 0)}
        Max: {flowrate.get('max', 0)}
        Std Dev: {flowrate.get('std', 0)}
        """
        flowrate_label = QLabel(flowrate_text)
        self.stats_layout.addWidget(flowrate_label, 2, 0)
        
        # Pressure Stats
        pressure_title = QLabel("<b>Pressure Statistics</b>")
        self.stats_layout.addWidget(pressure_title, 1, 1)
        
        pressure = stats.get('pressure', {})
        pressure_text = f"""
        Mean: {pressure.get('mean', 0)}
        Min: {pressure.get('min', 0)}
        Max: {pressure.get('max', 0)}
        Std Dev: {pressure.get('std', 0)}
        """
        pressure_label = QLabel(pressure_text)
        self.stats_layout.addWidget(pressure_label, 2, 1)
        
        # Temperature Stats
        temperature_title = QLabel("<b>Temperature Statistics</b>")
        self.stats_layout.addWidget(temperature_title, 3, 0)
        
        temperature = stats.get('temperature', {})
        temperature_text = f"""
        Mean: {temperature.get('mean', 0)}
        Min: {temperature.get('min', 0)}
        Max: {temperature.get('max', 0)}
        Std Dev: {temperature.get('std', 0)}
        """
        temperature_label = QLabel(temperature_text)
        self.stats_layout.addWidget(temperature_label, 4, 0)
        
        # Equipment Types
        equipment_types_title = QLabel("<b>Equipment Types</b>")
        self.stats_layout.addWidget(equipment_types_title, 3, 1)
        
        equipment_types = stats.get('equipment_types', {})
        types_text = '\n'.join([f"{k}: {v}" for k, v in equipment_types.items()])
        types_label = QLabel(types_text)
        self.stats_layout.addWidget(types_label, 4, 1)
