"""
Utility functions for CSV processing, statistics computation, and PDF generation.
"""
import pandas as pd
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.conf import settings


def validate_csv_columns(df):
    """
    Validate that the CSV has required columns.
    Expected columns: Equipment Name, Type, Flowrate, Pressure, Temperature
    """
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    return True


def parse_csv_file(csv_file):
    """
    Parse uploaded CSV file into pandas DataFrame.
    Returns DataFrame or raises ValueError.
    """
    try:
        # Read CSV with pandas
        df = pd.read_csv(csv_file)
        
        # Validate columns
        validate_csv_columns(df)
        
        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()
        
        # Convert numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with all NaN values
        df = df.dropna(how='all')
        
        return df
    
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing CSV: {str(e)}")


def compute_summary_statistics(df):
    """
    Compute summary statistics from the DataFrame.
    Returns a dictionary with statistics.
    """
    stats = {
        'total_count': len(df),
        'equipment_types': df['Type'].value_counts().to_dict(),
        'flowrate': {
            'mean': round(df['Flowrate'].mean(), 2) if not df['Flowrate'].isna().all() else 0,
            'min': round(df['Flowrate'].min(), 2) if not df['Flowrate'].isna().all() else 0,
            'max': round(df['Flowrate'].max(), 2) if not df['Flowrate'].isna().all() else 0,
            'std': round(df['Flowrate'].std(), 2) if not df['Flowrate'].isna().all() else 0,
        },
        'pressure': {
            'mean': round(df['Pressure'].mean(), 2) if not df['Pressure'].isna().all() else 0,
            'min': round(df['Pressure'].min(), 2) if not df['Pressure'].isna().all() else 0,
            'max': round(df['Pressure'].max(), 2) if not df['Pressure'].isna().all() else 0,
            'std': round(df['Pressure'].std(), 2) if not df['Pressure'].isna().all() else 0,
        },
        'temperature': {
            'mean': round(df['Temperature'].mean(), 2) if not df['Temperature'].isna().all() else 0,
            'min': round(df['Temperature'].min(), 2) if not df['Temperature'].isna().all() else 0,
            'max': round(df['Temperature'].max(), 2) if not df['Temperature'].isna().all() else 0,
            'std': round(df['Temperature'].std(), 2) if not df['Temperature'].isna().all() else 0,
        },
    }
    
    return stats


def dataframe_to_dict(df):
    """
    Convert DataFrame to list of dictionaries for JSON storage.
    """
    # Replace NaN with None for JSON compatibility
    df_clean = df.where(pd.notnull(df), None)
    return df_clean.to_dict(orient='records')


def generate_pdf_report(dataset):
    """
    Generate a PDF report for the given dataset.
    Returns BytesIO buffer containing the PDF.
    """
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12,
        spaceBefore=12,
    )
    
    # Title
    title = Paragraph("Chemical Equipment Parameter Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Dataset Info
    info_data = [
        ['Dataset Information', ''],
        ['Filename:', dataset.filename],
        ['Upload Date:', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Records:', str(dataset.row_count)],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Summary Statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    elements.append(Spacer(1, 12))
    
    stats = dataset.summary_stats
    
    # Flowrate Stats
    flowrate_data = [
        ['Flowrate Statistics', ''],
        ['Mean:', f"{stats['flowrate']['mean']}"],
        ['Min:', f"{stats['flowrate']['min']}"],
        ['Max:', f"{stats['flowrate']['max']}"],
        ['Std Dev:', f"{stats['flowrate']['std']}"],
    ]
    
    flowrate_table = Table(flowrate_data, colWidths=[2*inch, 2*inch])
    flowrate_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(flowrate_table)
    elements.append(Spacer(1, 12))
    
    # Pressure Stats
    pressure_data = [
        ['Pressure Statistics', ''],
        ['Mean:', f"{stats['pressure']['mean']}"],
        ['Min:', f"{stats['pressure']['min']}"],
        ['Max:', f"{stats['pressure']['max']}"],
        ['Std Dev:', f"{stats['pressure']['std']}"],
    ]
    
    pressure_table = Table(pressure_data, colWidths=[2*inch, 2*inch])
    pressure_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(pressure_table)
    elements.append(Spacer(1, 12))
    
    # Temperature Stats
    temp_data = [
        ['Temperature Statistics', ''],
        ['Mean:', f"{stats['temperature']['mean']}"],
        ['Min:', f"{stats['temperature']['min']}"],
        ['Max:', f"{stats['temperature']['max']}"],
        ['Std Dev:', f"{stats['temperature']['std']}"],
    ]
    
    temp_table = Table(temp_data, colWidths=[2*inch, 2*inch])
    temp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#ef4444')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(temp_table)
    elements.append(Spacer(1, 20))
    
    # Equipment Type Distribution
    elements.append(Paragraph("Equipment Type Distribution", heading_style))
    elements.append(Spacer(1, 12))
    
    type_data = [['Equipment Type', 'Count']]
    for equip_type, count in stats['equipment_types'].items():
        type_data.append([str(equip_type), str(count)])
    
    type_table = Table(type_data, colWidths=[3*inch, 2*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#8b5cf6')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(type_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
