# =================================================================
# SISTEMA INTEGRADO DE AUDITORÍA DE PASIVOS CORRIENTES
# CON GENERACIÓN DE INFORMES PROFESIONALES
# Versión Final Completa
# =================================================================

import streamlit as st
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
from scipy.stats import zscore
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import base64

# =================================================================
# CONFIGURACIÓN DE PÁGINA
# =================================================================
st.set_page_config(
    page_title="Auditoría Pasivos Corrientes",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .module-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        padding: 0.5rem 0;
        border-left: 5px solid #1f77b4;
        padding-left: 1rem;
        margin: 1.5rem 0;
    }
    .report-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin: 2rem 0;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #155a8a;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# FUNCIONES DE GENERACIÓN DE DATOS
# =================================================================

@st.cache_data
def generar_cuentas_por_pagar():
    """Genera datos simulados de cuentas por pagar."""
    np.random.seed(42)
    num_registros = 50
    fecha_actual = datetime.now()

    ids_factura = [f'INV-{i:04d}' for i in range(num_registros)]
    proveedores = [f'Proveedor_{i}' for i in random.choices(range(1, 21), k=num_registros)]
    montos = [round(random.uniform(100, 75000), 2) for _ in range(num_registros)]
    monedas = random.choices(['USD', 'ARS', 'EUR'], weights=[0.5, 0.4, 0.1], k=num_registros)
    estados_posibles = ['Pendiente', 'Pagada', 'Vencida']

    fechas_emision = []
    fechas_vencimiento = []
    estados_final = []

    for _ in range(num_registros):
        emision = fecha_actual - timedelta(days=random.randint(10, 730))
        vencimiento_base = emision + timedelta(days=random.randint(5, 120))
        estado = random.choices(estados_posibles, weights=[0.65, 0.25, 0.10], k=1)[0]

        if estado == 'Vencida':
            vencimiento = fecha_actual - timedelta(days=random.randint(1, 180))
            if emision >= vencimiento:
                emision = vencimiento - timedelta(days=random.randint(5, 60))
        elif estado == 'Pendiente':
            vencimiento = fecha_actual + timedelta(days=random.randint(1, 90))
            if emision >= vencimiento:
                emision = vencimiento - timedelta(days=random.randint(5, 60))
        else:
            vencimiento = vencimiento_base

        fechas_emision.append(emision)
        fechas_vencimiento.append(vencimiento)
        estados_final.append(estado)

    return pd.DataFrame({
        'id_factura': ids_factura,
        'proveedor': proveedores,
        'fecha_emision': fechas_emision,
        'fecha_vencimiento': fechas_vencimiento,
        'monto': montos,
        'moneda': monedas,
        'estado': estados_final
    })


@st.cache_data
def analizar_cuentas_por_pagar(df):
    """Analiza cuentas por pagar."""
    df['fecha_emision'] = pd.to_datetime(df['fecha_emision'])
    df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento'])
    fecha_actual = datetime.now()
    
    df['dias_hasta_vencimiento'] = (df['fecha_vencimiento'] - fecha_actual).dt.days
    df['monto_zscore'] = zscore(df['monto'])
    
    features = df[['monto', 'dias_hasta_vencimiento']].fillna(0)
    iso_forest = IsolationForest(random_state=42, contamination=0.1)
    df['is_anomaly'] = iso_forest.fit_predict(features)
    
    return df


@st.cache_data
def generar_prestamos():
    """Genera datos de préstamos."""
    np.random.seed(42)
    num_prestamos = 50
    
    data = []
    for i in range(num_prestamos):
        data.append({
            'ID_Prestamo': f'LOAN-{i+1:04d}',
            'Fecha_Obtencion': datetime.now() - timedelta(days=random.randint(0, 730)),
            'Monto_Prestamo': round(random.uniform(10000, 500000), 2),
            'Tasa_Interes_Anual': round(random.uniform(0.05, 0.20), 4),
            'Plazo_Meses': random.randint(12, 61),
            'Estado_Pago': random.choice(['Activo', 'Pagado', 'Atrasado', 'Cancelado'])
        })
    
    return pd.DataFrame(data)


@st.cache_data
def generar_remuneraciones():
    """Genera datos de nómina."""
    np.random.seed(123)
    fake = Faker('es_AR')
    Faker.seed(123)
    
    departamentos = ['Ventas', 'Marketing', 'Finanzas', 'Operaciones', 'IT', 'RRHH']
    datos = []
    
    for i in range(100):
        departamento = random.choice(departamentos)
        salario_bruto = round(random.uniform(50000, 300000), 2)
        
        datos.append({
            'ID_Empleado': f'EMP-{i+1:04d}',
            'Nombre': fake.name(),
            'Departamento': departamento,
            'Salario_Bruto': salario_bruto,
            'Aportes_Patronales': salario_bruto * 0.23,
            'Salario_Neto': salario_bruto * 0.83
        })
    
    return pd.DataFrame(datos)


@st.cache_data
def generar_cargas_fiscales():
    """Genera obligaciones fiscales."""
    np.random.seed(42)
    
    tipos = ['IVA', 'Ganancias', 'Ingresos Brutos', 'Aportes', 'Bienes Personales']
    estados = ['Pendiente', 'Pagado', 'Vencido']
    
    data = []
    for i in range(50):
        tipo = random.choice(tipos)
        fecha_venc = datetime.now() + timedelta(days=random.randint(-90, 90))
        
        data.append({
            'id_impuesto': f'IMP-{i:04d}',
            'tipo_impuesto': tipo,
            'fecha_vencimiento': fecha_venc,
            'monto_ars': round(random.uniform(50000, 5000000), 2),
            'estado_pago': random.choice(estados)
        })
    
    return pd.DataFrame(data)


@st.cache_data
def generar_datos_consolidados():
    """Genera todos los datos para el informe consolidado."""
    return {
        'cuentas': analizar_cuentas_por_pagar(generar_cuentas_por_pagar()),
        'prestamos': generar_prestamos(),
        'remuneraciones': generar_remuneraciones(),
        'fiscales': generar_cargas_fiscales()
    }


# =================================================================
# FUNCIONES DE GENERACIÓN DE REPORTES
# =================================================================

def crear_informe_pdf_simple(datos):
    """Genera un informe PDF simple."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph("INFORME DE AUDITORÍA", title_style))
    story.append(Paragraph("PASIVOS CORRIENTES", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Fecha de generación: {fecha_actual}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("1. RESUMEN EJECUTIVO", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    df_cuentas = datos['cuentas']
    df_prestamos = datos['prestamos']
    df_rrhh = datos['remuneraciones']
    df_fiscales = datos['fiscales']
    
    resumen_data = [
        ['CATEGORÍA', 'CANTIDAD', 'MONTO TOTAL ($)'],
        ['Cuentas por Pagar', 
         str(len(df_cuentas[df_cuentas['estado'] == 'Pendiente'])),
         f"{df_cuentas[df_cuentas['estado'] == 'Pendiente']['monto'].sum():,.2f}"],
        ['Préstamos Activos', 
         str(len(df_prestamos[df_prestamos['Estado_Pago'] == 'Activo'])),
         f"{df_prestamos[df_prestamos['Estado_Pago'] == 'Activo']['Monto_Prestamo'].sum():,.2f}"],
        ['Nómina Mensual', 
         str(len(df_rrhh)),
         f"{df_rrhh['Salario_Bruto'].sum():,.2f}"],
        ['Cargas Fiscales', 
         str(len(df_fiscales[df_fiscales['estado_pago'] == 'Pendiente'])),
         f"{df_fiscales[df_fiscales['estado_pago'] == 'Pendiente']['monto_ars'].sum():,.2f}"]
    ]
    
    tabla_resumen = Table(resumen_data, colWidths=[3*inch, 1.5*inch, 2*inch])
    tabla_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(tabla_resumen)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def crear_informe_excel(datos):
    """Genera un informe Excel."""
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#1f77b4',
            'font_color': 'white',
            'border': 1
        })
        
        resumen_data = {
            'Categoría': ['Cuentas por Pagar', 'Préstamos', 'Nómina', 'Cargas Fiscales'],
            'Cantidad_Registros': [
                len(datos['cuentas'][datos['cuentas']['estado'] == 'Pendiente']),
                len(datos['prestamos'][datos['prestamos']['Estado_Pago'] == 'Activo']),
                len(datos['remuneraciones']),
                len(datos['fiscales'][datos['fiscales']['estado_pago'] == 'Pendiente'])
            ],
            'Monto_Total': [
                datos['cuentas'][datos['cuentas']['estado'] == 'Pendiente']['monto'].sum(),
                datos['prestamos'][datos['prestamos']['Estado_Pago'] == 'Activo']['Monto_Prestamo'].sum(),
                datos['remuneraciones']['Salario_Bruto'].sum(),
                datos['fiscales'][datos['fiscales']['estado_pago'] == 'Pendiente']['monto_ars'].sum()
            ]
        }
        
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
        
        datos['cuentas'].to_excel(writer, sheet_name='Cuentas_por_Pagar', index=False)
        datos['prestamos'].to_excel(writer, sheet_name='Prestamos', index=False)
        datos['remuneraciones'].to_excel(writer, sheet_name='Remuneraciones', index=False)
        datos['fiscales'].to_excel(writer, sheet_name='Cargas_Fiscales', index=False)
    
    buffer.seek(0)
    return buffer


def crear_informe_auditoria_normas(datos):
    """Genera informe profesional con normas RT 7, RT 37 y NIAs."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=15,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        borderWidth=2,
        borderColor=colors.HexColor('#1f77b4'),
        borderPadding=5,
        backColor=colors.HexColor('#e8f4f8')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )
    
    fecha_actual = datetime.now()
    fecha_str = fecha_actual.strftime("%d de %B de %Y")
    
    story.append(Paragraph("INFORME DE AUDITORÍA", title_style))
    story.append(Paragraph("SOBRE PASIVOS CORRIENTES", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    info_data = [
        ['Empresa Auditada:', 'EMPRESA EJEMPLO S.A.'],
        ['CUIT:', '30-12345678-9'],
        ['Período Auditado:', f'{fecha_actual.strftime("%m/%Y")}'],
        ['Fecha del Informe:', fecha_str],
        ['Normas Aplicadas:', 'RT 7, RT 37, NIAs']
    ]
    
    tabla_info = Table(info_data, colWidths=[2.5*inch, 4*inch])
    tabla_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(tabla_info)
    story.append(Spacer(1, 0.4*inch))
    
    # I. IDENTIFICACIÓN
    story.append(Paragraph("I. IDENTIFICACIÓN DEL ENTE Y PERÍODO AUDITADO", subtitle_style))
    story.append(Spacer(1, 0.1*inch))
    
    texto_id = f"""Hemos auditado los pasivos corrientes de <b>EMPRESA EJEMPLO S.A.</b>, 
    CUIT 30-12345678-9, correspondientes al período finalizado el {fecha_str}. La auditoría 
    se realizó conforme a las <b>Normas Internacionales de Auditoría (NIAs)</b> y las 
    <b>Resoluciones Técnicas 7 y 37</b> de FACPCE."""
    
    story.append(Paragraph(texto_id, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # II. ALCANCE
    story.append(Paragraph("II. ALCANCE DEL TRABAJO", subtitle_style))
    story.append(Paragraph("2.1. Procedimientos Aplicados (Según RT 7)", heading_style))
    
    procedimientos = [
        "• Confirmaciones externas de saldos con proveedores y acreedores",
        "• Inspección de documentación respaldatoria",
        "• Pruebas de corte de operaciones",
        "• Análisis de antigüedad de saldos",
        "• Revisión de conciliaciones bancarias",
        "• Verificación de cálculos de intereses y cargas sociales",
        "• Evaluación de controles internos",
        "• Pruebas sustantivas de transacciones",
        "• Análisis de eventos posteriores"
    ]
    
    for proc in procedimientos:
        story.append(Paragraph(proc, body_style))
    
    story.append(PageBreak())
    
    # III. RESUMEN DE HALLAZGOS
    story.append(Paragraph("III. RESUMEN DE HALLAZGOS", subtitle_style))
    
    df_cuentas = datos['cuentas']
    df_prestamos = datos['prestamos']
    df_rrhh = datos['remuneraciones']
    df_fiscales = datos['fiscales']
    
    total_pasivos = (
        df_cuentas[df_cuentas['estado'] == 'Pendiente']['monto'].sum() +
        df_prestamos[df_prestamos['Estado_Pago'] == 'Activo']['Monto_Prestamo'].sum() +
        df_rrhh['Salario_Bruto'].sum() +
        df_fiscales[df_fiscales['estado_pago'] == 'Pendiente']['monto_ars'].sum()
    )
    
    resumen_data = [
        ['RUBRO', 'CANTIDAD', 'SALDO ($)', '% TOTAL'],
        ['Cuentas por Pagar',
         str(len(df_cuentas[df_cuentas['estado'] == 'Pendiente'])),
         f"{df_cuentas[df_cuentas['estado'] == 'Pendiente']['monto'].sum():,.2f}",
         f"{(df_cuentas[df_cuentas['estado'] == 'Pendiente']['monto'].sum() / total_pasivos * 100):.1f}%"],
        ['Préstamos',
         str(len(df_prestamos[df_prestamos['Estado_Pago'] == 'Activo'])),
         f"{df_prestamos[df_prestamos['Estado_Pago'] == 'Activo']['Monto_Prestamo'].sum():,.2f}",
         f"{(df_prestamos[df_prestamos['Estado_Pago'] == 'Activo']['Monto_Prestamo'].sum() / total_pasivos * 100):.1f}%"],
        ['Remuneraciones',
         str(len(df_rrhh)),
         f"{df_rrhh['Salario_Bruto'].sum():,.2f}",
         f"{(df_rrhh['Salario_Bruto'].sum() / total_pasivos * 100):.1f}%"],
        ['Cargas Fiscales',
         str(len(df_fiscales[df_fiscales['estado_pago'] == 'Pendiente'])),
         f"{df_fiscales[df_fiscales['estado_pago'] == 'Pendiente']['monto_ars'].sum():,.2f}",
         f"{(df_fiscales[df_fiscales['estado_pago'] == 'Pendiente']['monto_ars'].sum() / total_pasivos * 100):.1f}%"],
        ['TOTAL', '', f"{total_pasivos:,.2f}", '100.0%']
    ]
    
    tabla_resumen = Table(resumen_data, colWidths=[2.5*inch, 1*inch, 1.8*inch, 1*inch])
    tabla_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f4f8')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
    ]))
    
    story.append(tabla_resumen)
    story.append(Spacer(1, 0.3*inch))
    
    # IV. HALLAZGOS ESPECÍFICOS
    story.append(Paragraph("IV. HALLAZGOS ESPECÍFICOS", subtitle_style))
    
    facturas_vencidas = len(df_cuentas[df_cuentas['estado'] == 'Vencida'])
    anomalias = (df_cuentas['is_anomaly'] == -1).sum()
    
    hallazgo = f"""<b>Cuentas por Pagar:</b> Se identificaron {facturas_vencidas} facturas 
    vencidas y {anomalias} transacciones con características atípicas.<br/><br/>
    <b>Recomendación (RT 7):</b> Implementar sistema de alertas tempranas para vencimientos."""
    
    story.append(Paragraph(hallazgo, body_style))
    story.append(PageBreak())
    
    # VII. OPINIÓN
    story.append(Paragraph("VII. OPINIÓN PROFESIONAL", subtitle_style))
    
    opinion = f"""En nuestra opinión, basada en la auditoría realizada conforme a las NIAs 
    y RT 7 y 37, los pasivos corrientes de EMPRESA EJEMPLO S.A. al {fecha_str}, por un total 
    de ${total_pasivos:,.2f}, se presentan razonablemente en todos sus aspectos significativos."""
    
    story.append(Paragraph(opinion, body_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Firma
    firma_data = [
        ['_____________________________', '_____________________________'],
        ['Contador Público', 'Socio Director'],
        ['CPCECABA T° XXX F° XXX', 'Estudio Contable'],
        ['Buenos Aires, ' + fecha_str, '']
    ]
    
    tabla_firma = Table(firma_data, colWidths=[3*inch, 3*inch])
    tabla_firma.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    
    story.append(tabla_firma)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


# =================================================================
# FUNCIONES DE VISUALIZACIÓN
# =================================================================

def crear_grafico_barras(data, x, y, titulo, color='viridis'):
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.Series):
        sns.barplot(x=data.index, y=data.values, palette=color, ax=ax)
    else:
        sns.barplot(data=data, x=x, y=y, palette=color, ax=ax)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def crear_grafico_torta(data, titulo):
    fig, ax = plt.subplots(figsize=(8, 8))
    colors_palette = sns.color_palette("Set2")
    data.plot(kind='pie', autopct='%1.1f%%', startangle=90, 
              colors=colors_palette, ax=ax, textprops={'fontsize': 10})
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('')
    plt.tight_layout()
    return fig


def mostrar_metricas(col, titulo, valor, delta=None, invertir=False):
    with col:
        if delta:
            st.metric(titulo, valor, delta=delta, delta_color="inverse" if invertir else "normal")
        else:
            st.metric(titulo, valor)


# =================================================================
# INTERFAZ PRINCIPAL
# =================================================================

def main():
    st.markdown('<h1 class="main-header">💼 Sistema de Auditoría de Pasivos Corrientes</h1>', 
                unsafe_allow_html=True)
    
    st.sidebar.title("📋 Menú de Navegación")
    st.sidebar.markdown("---")
    
    modulo = st.sidebar.radio(
        "Seleccione un módulo:",
        [
            "🏠 Inicio",
            "📊 Dashboard General",
            "📄 Generación de Informes",
            "📋 Cuentas por Pagar",
            "💰 Préstamos Obtenidos",
            "👥 Remuneraciones",
            "🏛️ Cargas Fiscales"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Nota:** Todos los datos son simulados con fines educativos.")
    
    # PÁGINA DE INICIO
    if modulo == "🏠 Inicio":
        st.markdown('<h2 class="module-header">Bienvenido al Sistema de Auditoría</h2>', 
                    unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 🎯 Sobre este Sistema
            
            Sistema profesional para **auditoría y análisis** de pasivos corrientes empresariales.
            
            #### 📌 Características:
            
            - ✅ **7 Módulos Especializados**
            - ✅ **Detección Automática de Anomalías**
            - ✅ **Visualizaciones Interactivas**
            - ✅ **3 Tipos de Informes Profesionales**:
              - 📑 Informe PDF Consolidado
              - 📊 Informe Excel Detallado
              - 📋 Informe de Auditoría con Normas (RT 7, RT 37, NIAs)
            
            #### 🔍 Módulos:
            
            1. **Cuentas por Pagar** - Gestión de facturas
            2. **Préstamos Obtenidos** - Control de deuda
            3. **Remuneraciones** - Análisis de nómina
            4. **Cargas Fiscales** - Obligaciones tributarias
            5. **Generación de Informes** - Reportes automáticos
            """)
        
        with col2:
            st.markdown("### 📊 Estadísticas")
            st.info("**Módulos:** 7")
            st.success("**Estado:** Operativo")
            st.warning("**Datos:** Simulados")
            
            st.markdown("---")
            st.markdown("### 🚀 Inicio Rápido")
            st.markdown("""
            1. Seleccione un módulo
            2. Haga clic en "Iniciar Análisis"
            3. Explore resultados
            4. Genere informes
            """)
            
            st.success("✨ **NUEVO:** Informes con normas profesionales RT 7, RT 37 y NIAs")
    
    # GENERACIÓN DE INFORMES
    elif modulo == "📄 Generación de Informes":
        st.markdown('<h2 class="module-header">📄 Generación de Informes de Auditoría</h2>', 
                    unsafe_allow_html=True)
        
        st.markdown("""
        <div class="report-section">
            <h3>🎯 Centro de Informes</h3>
            <p>Genere informes profesionales de auditoría en formato PDF o Excel.</p>
            <p>Incluye análisis detallado, hallazgos, recomendaciones y normas profesionales.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Informe Consolidado")
            st.markdown("""
            **Incluye:**
            - ✅ Resumen ejecutivo
            - ✅ Métricas principales
            - ✅ Hallazgos clave
            """)
            
            if st.button("📑 PDF Consolidado"):
                with st.spinner("Generando..."):
                    datos = generar_datos_consolidados()
                    pdf_buffer = crear_informe_pdf_simple(datos)
                    st.success("✅ Generado")
                    st.download_button(
                        "⬇️ Descargar PDF",
                        pdf_buffer,
                        f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf"
                    )
        
        with col2:
            st.markdown("### 📈 Informe Excel")
            st.markdown("""
            **Incluye:**
            - ✅ Múltiples hojas
            - ✅ Datos detallados
            - ✅ Formato profesional
            """)
            
            if st.button("📊 Excel Detallado"):
                with st.spinner("Generando..."):
                    datos = generar_datos_consolidados()
                    excel_buffer = crear_informe_excel(datos)
                    st.success("✅ Generado")
                    st.download_button(
                        "⬇️ Descargar Excel",
                        excel_buffer,
                        f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        with col3:
            st.markdown("### 📋 Informe Profesional")
            st.markdown("""
            **Incluye:**
            - ✅ Normas RT 7, RT 37, NIAs
            - ✅ Procedimientos
            - ✅ Opinión profesional
            """)
            
            if st.button("📑 Informe con Normas"):
                with st.spinner("Generando informe profesional..."):
                    datos = generar_datos_consolidados()
                    pdf_buffer = crear_informe_auditoria_normas(datos)
                    st.success("✅ Generado")
                    st.download_button(
                        "⬇️ Descargar Informe Profesional",
                        pdf_buffer,
                        f"informe_auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf"
                    )
    
    # DASHBOARD GENERAL
    elif modulo == "📊 Dashboard General":
        st.markdown('<h2 class="module-header">Dashboard General</h2>', unsafe_allow_html=True)
        
        if st.button("🔄 Generar Dashboard"):
            with st.spinner("Generando..."):
                datos = generar_datos_consolidados()
                df_cuentas = datos['cuentas']
                df_prestamos = datos['prestamos']
                df_rrhh = datos['remuneraciones']
                df_fiscales = datos['fiscales']
                
                st.success("✅ Dashboard generado")
                
                col1, col2, col3, col4 = st.columns(4)
                mostrar_metricas(col1, "Facturas Pendientes", 
                               len(df_cuentas[df_cuentas['estado'] == 'Pendiente']))
                mostrar_metricas(col2, "Préstamos Activos", 
                               len(df_prestamos[df_prestamos['Estado_Pago'] == 'Activo']))
                mostrar_metricas(col3, "Empleados", len(df_rrhh))
                mostrar_metricas(col4, "Impuestos Pendientes", 
                               len(df_fiscales[df_fiscales['estado_pago'] == 'Pendiente']))
                
                st.markdown("---")
                st.markdown("### 📈 Análisis Consolidado")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    categorias = ['Cuentas\npor Pagar', 'Préstamos', 'Nómina', 'Fiscales']
                    valores = [
                        df_cuentas[df_cuentas['estado'] == 'Pendiente']['monto'].sum(),
                        df_prestamos[df_prestamos['Estado_Pago'] == 'Activo']['Monto_Prestamo'].sum(),
                        df_rrhh['Salario_Bruto'].sum(),
                        df_fiscales[df_fiscales['estado_pago'] == 'Pendiente']['monto_ars'].sum()
                    ]
                    
                    fig1, ax1 = plt.subplots(figsize=(10, 6))
                    sns.barplot(x=categorias, y=valores, palette='viridis', ax=ax1)
                    ax1.set_title('Distribución por Categoría', fontsize=14, fontweight='bold')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig1)
                
                with col2:
                    data_top = pd.DataFrame({'Categoría': categorias, 'Monto': valores})
                    fig2 = crear_grafico_torta(data_top.set_index('Categoría')['Monto'], 
                                               'Composición de Pasivos')
                    st.pyplot(fig2)
    
    # CUENTAS POR PAGAR
    elif modulo == "📋 Cuentas por Pagar":
        st.markdown('<h2 class="module-header">Cuentas por Pagar</h2>', unsafe_allow_html=True)
        
        if st.button("🔍 Iniciar Análisis"):
            with st.spinner("Analizando..."):
                df = generar_cuentas_por_pagar()
                df_auditado = analizar_cuentas_por_pagar(df)
                st.success("✅ Análisis completado")
                
                col1, col2, col3, col4 = st.columns(4)
                mostrar_metricas(col1, "Total Facturas", f"{len(df_auditado)}")
                mostrar_metricas(col2, "Monto Pendiente", 
                               f"${df_auditado[df_auditado['estado'] == 'Pendiente']['monto'].sum():,.2f}")
                mostrar_metricas(col3, "Vencidas", 
                               f"{len(df_auditado[df_auditado['estado'] == 'Vencida'])}")
                mostrar_metricas(col4, "Anomalías", f"{(df_auditado['is_anomaly'] == -1).sum()}")
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    monto_prov = df_auditado.groupby('proveedor')['monto'].sum().sort_values(ascending=False).head(10)
                    fig1 = crear_grafico_barras(monto_prov, None, None, 'Top 10 Proveedores', 'Blues_d')
                    st.pyplot(fig1)
                
                with col2:
                    estado_count = df_auditado['estado'].value_counts()
                    fig2 = crear_grafico_torta(estado_count, 'Distribución por Estado')
                    st.pyplot(fig2)
                
                st.markdown("### 📋 Detalle")
                st.dataframe(df_auditado.head(20), use_container_width=True)
    
    # PRÉSTAMOS
    elif modulo == "💰 Préstamos Obtenidos":
        st.markdown('<h2 class="module-header">Préstamos Obtenidos</h2>', unsafe_allow_html=True)
        
        if st.button("🔍 Iniciar Análisis"):
            with st.spinner("Analizando..."):
                df = generar_prestamos()
                st.success("✅ Análisis completado")
                
                col1, col2, col3, col4 = st.columns(4)
                mostrar_metricas(col1, "Total", f"{len(df)}")
                mostrar_metricas(col2, "Monto Total", f"${df['Monto_Prestamo'].sum():,.2f}")
                mostrar_metricas(col3, "Activos", f"{len(df[df['Estado_Pago'] == 'Activo'])}")
                mostrar_metricas(col4, "Tasa Prom", f"{df['Tasa_Interes_Anual'].mean():.2%}")
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1, ax1 = plt.subplots(figsize=(10, 6))
                    sns.histplot(df['Monto_Prestamo'], bins=15, kde=True, color='steelblue', ax=ax1)
                    ax1.set_title('Distribución de Montos')
                    plt.tight_layout()
                    st.pyplot(fig1)
                
                with col2:
                    fig2 = crear_grafico_torta(df['Estado_Pago'].value_counts(), 'Por Estado')
                    st.pyplot(fig2)
                
                st.dataframe(df.head(20), use_container_width=True)
    
    # REMUNERACIONES
    elif modulo == "👥 Remuneraciones":
        st.markdown('<h2 class="module-header">Remuneraciones</h2>', unsafe_allow_html=True)
        
        if st.button("🔍 Iniciar Análisis"):
            with st.spinner("Analizando..."):
                df = generar_remuneraciones()
                st.success("✅ Análisis completado")
                
                col1, col2, col3, col4 = st.columns(4)
                mostrar_metricas(col1, "Empleados", f"{len(df)}")
                mostrar_metricas(col2, "Salarios", f"${df['Salario_Bruto'].sum():,.2f}")
                mostrar_metricas(col3, "Aportes", f"${df['Aportes_Patronales'].sum():,.2f}")
                mostrar_metricas(col4, "Carga Total", 
                               f"${(df['Salario_Bruto'].sum() + df['Aportes_Patronales'].sum()):,.2f}")
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1, ax1 = plt.subplots(figsize=(10, 6))
                    sns.boxplot(data=df, x='Departamento', y='Salario_Bruto', palette='Set2', ax=ax1)
                    ax1.set_title('Por Departamento')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig1)
                
                with col2:
                    cargas = df.groupby('Departamento').agg({
                        'Salario_Bruto': 'sum',
                        'Aportes_Patronales': 'sum'
                    }).reset_index()
                    cargas['Carga_Total'] = cargas['Salario_Bruto'] + cargas['Aportes_Patronales']
                    fig2 = crear_grafico_barras(cargas, 'Departamento', 'Carga_Total',
                                               'Carga Social Total', 'Reds_d')
                    st.pyplot(fig2)
                
                st.dataframe(cargas, use_container_width=True)
    
    # CARGAS FISCALES
    elif modulo == "🏛️ Cargas Fiscales":
        st.markdown('<h2 class="module-header">Cargas Fiscales</h2>', unsafe_allow_html=True)
        
        if st.button("🔍 Iniciar Análisis"):
            with st.spinner("Analizando..."):
                df = generar_cargas_fiscales()
                st.success("✅ Análisis completado")
                
                col1, col2, col3, col4 = st.columns(4)
                mostrar_metricas(col1, "Obligaciones", f"{len(df)}")
                mostrar_metricas(col2, "Monto Total", f"${df['monto_ars'].sum():,.2f}")
                mostrar_metricas(col3, "Pendientes", f"{len(df[df['estado_pago'] == 'Pendiente'])}")
                mostrar_metricas(col4, "Vencidos", f"{len(df[df['estado_pago'] == 'Vencido'])}")
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    monto_tipo = df.groupby('tipo_impuesto')['monto_ars'].sum().sort_values(ascending=False)
                    fig1 = crear_grafico_barras(monto_tipo, None, None, 'Por Tipo', 'Greens_d')
                    st.pyplot(fig1)
                
                with col2:
                    fig2 = crear_grafico_torta(df['estado_pago'].value_counts(), 'Por Estado')
                    st.pyplot(fig2)
                
                st.dataframe(df.head(20), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>Sistema de Auditoría de Pasivos Corrientes v1.0</strong></p>
        <p>Informes con normas RT 7, RT 37 y NIAs</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
