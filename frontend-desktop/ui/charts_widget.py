from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ChartsWidget(QWidget):
    """Widget for displaying charts using Matplotlib"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.summary = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('Data Visualizations')
        title.setStyleSheet('font-size: 16px; font-weight: bold; margin: 10px;')
        layout.addWidget(title)
        
        # Grid for charts
        self.charts_layout = QGridLayout()
        layout.addLayout(self.charts_layout)
        
        self.setLayout(layout)
    
    def load_data(self, data, summary):
        """Load and display charts"""
        self.data = data
        self.summary = summary
        
        # Clear previous charts
        for i in reversed(range(self.charts_layout.count())): 
            self.charts_layout.itemAt(i).widget().setParent(None)
        
        if not data or not summary:
            return
        
        # Create charts
        flowrate_chart = self.create_flowrate_chart()
        pressure_chart = self.create_pressure_chart()
        temperature_chart = self.create_temperature_chart()
        type_distribution_chart = self.create_type_distribution_chart()
        
        # Add to grid
        self.charts_layout.addWidget(flowrate_chart, 0, 0)
        self.charts_layout.addWidget(pressure_chart, 0, 1)
        self.charts_layout.addWidget(temperature_chart, 1, 0)
        self.charts_layout.addWidget(type_distribution_chart, 1, 1)
    
    def create_flowrate_chart(self):
        """Create flowrate bar chart"""
        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        equipment_names = [row.get('Equipment Name', f'Eq {i}') for i, row in enumerate(self.data)]
        flowrates = [row.get('Flowrate', 0) for row in self.data]
        
        ax.bar(range(len(flowrates)), flowrates, color='#10b981')
        ax.set_title('Flowrate Distribution')
        ax.set_xlabel('Equipment')
        ax.set_ylabel('Flowrate')
        ax.set_xticks(range(len(equipment_names)))
        ax.set_xticklabels(equipment_names, rotation=45, ha='right')
        
        figure.tight_layout()
        return canvas
    
    def create_pressure_chart(self):
        """Create pressure line chart"""
        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        pressures = [row.get('Pressure', 0) for row in self.data]
        
        ax.plot(pressures, marker='o', color='#f59e0b', linewidth=2)
        ax.set_title('Pressure Trend')
        ax.set_xlabel('Equipment Index')
        ax.set_ylabel('Pressure')
        ax.grid(True, alpha=0.3)
        
        figure.tight_layout()
        return canvas
    
    def create_temperature_chart(self):
        """Create temperature line chart"""
        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        temperatures = [row.get('Temperature', 0) for row in self.data]
        
        ax.plot(temperatures, marker='s', color='#ef4444', linewidth=2)
        ax.set_title('Temperature Trend')
        ax.set_xlabel('Equipment Index')
        ax.set_ylabel('Temperature')
        ax.grid(True, alpha=0.3)
        
        figure.tight_layout()
        return canvas
    
    def create_type_distribution_chart(self):
        """Create equipment type distribution pie chart"""
        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        equipment_types = self.summary.get('equipment_types', {})
        labels = list(equipment_types.keys())
        sizes = list(equipment_types.values())
        colors = ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#ec4899']
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Equipment Type Distribution')
        ax.axis('equal')
        
        figure.tight_layout()
        return canvas
