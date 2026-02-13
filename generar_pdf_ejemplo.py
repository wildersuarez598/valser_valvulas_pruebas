import os
import django
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Crear PDF de certificado de ejemplo
pdf_path = 'certificado_ejemplo.pdf'

# Estilos
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=12,
    fontName='Helvetica-Bold'
)

# Crear documento
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
elements = []

# Título
elements.append(Paragraph("CERTIFICADO DE CALIBRACIÓN", title_style))
elements.append(Spacer(1, 0.2*inch))

# Información del certificado
cert_data = [
    ['Número de Certificado:', 'CERT-2026-001'],
    ['Tipo de Certificado:', 'Calibración'],
    ['Fecha de Emisión:', '13/02/2026'],
    ['Fecha de Vencimiento:', '13/02/2027'],
]

cert_table = Table(cert_data, colWidths=[2*inch, 4*inch])
cert_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

elements.append(cert_table)
elements.append(Spacer(1, 0.3*inch))

# Datos Técnicos
elements.append(Paragraph("DATOS TÉCNICOS", heading_style))

tech_data = [
    ['Presión Inicial:', '50 PSI', 'Presión Final:', '50 PSI'],
    ['Temperatura:', '25°C', 'Resultado:', 'APROBADO'],
]

tech_table = Table(tech_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

elements.append(tech_table)
elements.append(Spacer(1, 0.3*inch))

# Información del Laboratorio
elements.append(Paragraph("INFORMACIÓN DEL LABORATORIO", heading_style))

lab_data = [
    ['Laboratorio:', 'LABORATORIO DE CALIBRACIÓN NACIONAL'],
    ['Técnico Responsable:', 'ING. JUAN CARLOS PÉREZ SOLANO'],
    ['Dirección:', 'Calle Principal 123, Bogotá - Colombia'],
]

lab_table = Table(lab_data, colWidths=[2*inch, 4*inch])
lab_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

elements.append(lab_table)
elements.append(Spacer(1, 0.3*inch))

# Notas
elements.append(Paragraph("NOTAS Y OBSERVACIONES", heading_style))
elements.append(Paragraph(
    "El equipo ha sido calibrado según normas internacionales ISO 9001:2015. "
    "Se ha verificado su funcionamiento en condiciones normales de operación. "
    "El certificado es válido por 12 meses a partir de la fecha de emisión.",
    styles['BodyText']
))

# Pie de página
elements.append(Spacer(1, 0.5*inch))
elements.append(Paragraph(
    "Este documento certifica que el equipo mencionado ha sido calibrado "
    "por personal especializado bajo estrictos estándares de calidad.",
    ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
))

# Crear PDF
doc.build(elements)
print(f"✓ PDF de ejemplo creado: {pdf_path}")
print(f"  Ubicación: {os.path.abspath(pdf_path)}")
print(f"\n¡Descarga este archivo y pruébalo en la interfaz!")
