"""
Extractores modulares para diferentes tipos de documentos (PDF)
Soporta: Certificados de Calibración e Informes de Mantenimiento
"""

import re
import pdfplumber
from typing import Dict, Optional, Tuple


class PDFExtractor:
    """Base para extractores de PDF"""
    
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.full_text = self._extract_text()
    
    def _extract_text(self) -> str:
        """Extrae texto de todo el PDF"""
        try:
            with pdfplumber.open(self.pdf_file) as pdf:
                return '\n'.join(page.extract_text() or '' for page in pdf.pages)
        except Exception as e:
            raise ValueError(f"Error extrayendo texto del PDF: {str(e)}")
    
    def find_pattern(self, *patterns: str) -> Optional[str]:
        """
        Busca múltiples patrones regex y retorna el primero encontrado
        
        Args:
            *patterns: Patrones regex a buscar en orden de preferencia
            
        Returns:
            Valor encontrado o None
        """
        for pattern in patterns:
            match = re.search(pattern, self.full_text, re.IGNORECASE | re.MULTILINE)
            if match:
                result = match.group(1).strip()
                return result if result else None
        return None
    
    def find_all_patterns(self, pattern: str, limit: int = 5) -> list:
        """Busca múltiples ocurrencias de un patrón"""
        matches = re.findall(pattern, self.full_text, re.IGNORECASE | re.MULTILINE)
        return [m.strip() for m in matches[:limit] if m.strip()]


class CertificadoCalibracionExtractor(PDFExtractor):
    """Extractor para certificados de calibración"""
    
    def detect(self) -> bool:
        """Detecta si el PDF es un certificado de calibración"""
        keywords = [
            'calibración', 'calibracion', 'calibration',
            'certificado', 'certificate',
            'presión', 'presion', 'pressure',
            'calibrado', 'calibrated'
        ]
        text_lower = self.full_text.lower()
        return sum(1 for kw in keywords if kw in text_lower) >= 2
    
    def extract(self) -> Dict:
        """Extrae datos de certificado de calibración"""
        return {
            'tipo_documento': 'calibracion',
            'numero_documento': self.find_pattern(
                r'(?:CERT|Certificado|Calibración|Certificate)[\s:]*([A-Z0-9\-\/]+)',
                r'(?:N|Nº|No)\.?[\s:]*([A-Z0-9\-\/]+)',
                r'Número[\s:]*([A-Z0-9\-\/]+)'
            ),
            'numero_serie': self.find_pattern(
                r'(?:Número[\s]de[\s]Serie|Serial[\s]Number|S/N|SN)[\s:]*([A-Z0-9\-]+)',
                r'(?:Serie)[\s:]*([A-Z0-9\-]+)',
                r'(?:Válvula)[\s:]*([A-Z0-9\-]+)'
            ),
            'fecha_emision': self.find_pattern(
                r'(?:Fecha|Emisión|Date|Emitted|FECHA)[\s:]*(\d{1,2}[\s\-\/\.]\d{1,2}[\s\-\/\.]\d{4})',
                r'(\d{4})[\s\-\/](\d{1,2})[\s\-\/](\d{1,2})',
                r'(\d{1,2}[\s\-\/\.]\d{1,2}[\s\-\/\.]\d{4})',  # Captura general de DD-MM-YYYY
            ),
            'fecha_vencimiento': self.find_pattern(
                r'(?:Vencimiento|Válido hasta|Expiration|Valid until|VENCIMIENTO)[\s:]*(\d{1,2}[\s\-\/\.]\d{1,2}[\s\-\/\.]\d{4})',
                r'(?:Próxima calibración|Next calibration)[\s:]*(\d{1,2}[\s\-\/\.]\d{1,2}[\s\-\/\.]\d{4})',
                r'(\d{1,2}[\s\-\/\.]\d{1,2}[\s\-\/\.]\d{4})',  # Captura general
            ),
            'presion_inicial': self.find_pattern(
                r'(?:Presión|Pressure)[\s]inicial[\s:]*([0-9.]+)',
                r'Initial[\s]Pressure[\s:]*([0-9.]+)',
                r'P\.?[\s]inicial[\s:]*([0-9.]+)'
            ),
            'presion_final': self.find_pattern(
                r'(?:Presión|Pressure)[\s]final[\s:]*([0-9.]+)',
                r'Final[\s]Pressure[\s:]*([0-9.]+)',
                r'P\.?[\s]final[\s:]*([0-9.]+)'
            ),
            'temperatura': self.find_pattern(
                r'(?:Temperatura|Temperature)[\s:]*([0-9\.\,]+)',
                r'T\.?[\s:]*([0-9\.\,]+)[\s]*(?:°?C|°?F)?'
            ),
            'resultado': self._extract_resultado(),
            'laboratorio': self.find_pattern(
                r'(?:Laboratorio|Laboratory|Lab)[\s:]*([^\n]+)',
                r'Acreditado por[\s:]*([^\n]+)'
            ),
            'tecnico_responsable': self.find_pattern(
                r'(?:Técnico|Technician|Responsable|Signed by)[\s:]*(?:de|)?[\s]*([A-Za-záéíóúñ\s]+)',
                r'Firma[\s:]*([A-Za-záéíóúñ\s]+)'
            ),
            'unidad_presion': self.find_pattern(
                r'(?:Presión[\s]inicial)[\s:]*[0-9.]+[\s]*(PSI|bar|atm|kPa)',
                r'Unidad[\s:]*([A-Z]+)'
            ),
        }
    
    def _extract_resultado(self) -> Optional[str]:
        """Extrae resultado de calibración con lógica mejorada"""
        # Patrones para resultado positivo
        si_patterns = [
            r'(?:Resultado|Result)[\s:]*(?:Sí|Aprobado|Conforme|Passed|OK|PASS)',
            r'(?:Cumple|Meets|Within[\s]tolerance)',
            r'Estado[\s:]*Aceptable'
        ]
        
        for pattern in si_patterns:
            if re.search(pattern, self.full_text, re.IGNORECASE):
                return 'APROBADO'
        
        # Patrones para resultado negativo
        no_patterns = [
            r'(?:Resultado|Result)[\s:]*(?:No|Rechazado|No[\s]conforme|Failed|FAIL)',
            r'(?:No[\s]cumple|Does[\s]not[\s]meet|Out[\s]of[\s]tolerance)',
            r'Estado[\s:]*Inaceptable'
        ]
        
        for pattern in no_patterns:
            if re.search(pattern, self.full_text, re.IGNORECASE):
                return 'RECHAZADO'
        
        return None


class InformeMantenimientoExtractor(PDFExtractor):
    """Extractor para informes de mantenimiento"""
    
    def detect(self) -> bool:
        """Detecta si el PDF es un informe de mantenimiento"""
        keywords = [
            'mantenimiento', 'maintenance',
            'informe', 'report', 'reporte',
            'servicio técnico', 'technical service',
            'revisión', 'inspection'
        ]
        text_lower = self.full_text.lower()
        return sum(1 for kw in keywords if kw in text_lower) >= 2
    
    def extract(self) -> Dict:
        """Extrae datos de informe de mantenimiento"""
        return {
            'tipo_documento': 'mantenimiento',
            'numero_documento': self.find_pattern(
                r'(?:Informe|Reporte|Report)[\s:]*([A-Z0-9\-\/]+)',
                r'(?:N|Nº|No)\.?[\s:]*([A-Z0-9\-\/]+)',
                r'Número[\s:]*([A-Z0-9\-\/]+)'
            ),
            'numero_serie': self.find_pattern(
                r'(?:Número[\s]de[\s]Serie|Serial[\s]Number|S/N|SN)[\s:]*([A-Z0-9\-]+)',
                r'(?:Serie)[\s:]*([A-Z0-9\-]+)',
                r'(?:Válvula)[\s:]*([A-Z0-9\-]+)'
            ),
            'fecha_mantenimiento': self.find_pattern(
                r'(?:Fecha|Mantenimiento|Date|Service[\s]Date)[\s:]*(\d{1,2}[\s\-\/]\d{1,2}[\s\-\/]\d{4})',
                r'(\d{4})\-(\d{2})\-(\d{2})'
            ),
            'tipo_mantenimiento': self.find_pattern(
                r'(?:Tipo|Tipo[\s]de[\s]Mantenimiento)[\s:]*([^\n]+)',
                r'(?:Preventivo|Correctivo|Inspección|Overhaul)',
                r'(?:Preventive|Corrective|Maintenance[\s]Type)[\s:]*([^\n]+)'
            ),
            'descripcion_trabajos': self.find_pattern(
                r'(?:Trabajos|Descripción|Work[\s]Done|Activities)[\s:]*([^\n]+)',
                r'(?:Se realizaron|Performed)[\s:]*([^\n]+)'
            ),
            'estado_valvula': self.find_pattern(
                r'(?:Estado|Condition)[\s:]*([^\n]+)',
                r'(?:Bueno|Defectuoso|Deteriorado|Good|Bad|Deteriorated)'
            ),
            'observaciones': self.find_pattern(
                r'(?:Observaciones|Notas|Notes|Remarks)[\s:]*([^\n]+)',
                r'(?:Comentarios)[\s:]*([^\n]+)'
            ),
            'proximo_mantenimiento': self.find_pattern(
                r'(?:Próximo|Próxima|Next)[\s](?:Mantenimiento|Maintenance)[\s:]*(\d{1,2}[\s\-\/]\d{1,2}[\s\-\/]\d{4})',
                r'(?:Programado para)[\s:]*(\d{1,2}[\s\-\/]\d{1,2}[\s\-\/]\d{4})'
            ),
            'tecnico_responsable': self.find_pattern(
                r'(?:Técnico|Responsable|Technician|Executed by)[\s:]*([A-Za-záéíóúñ\s]+)',
                r'Realizado por[\s:]*([A-Za-záéíóúñ\s]+)',
                r'Firma[\s:]*([A-Za-záéíóúñ\s]+)'
            ),
            'materiales_utilizados': ' '.join(self.find_all_patterns(
                r'(?:Material|Componente)[\s:]*([^\n]+)',
                limit=5
            )),
            'duracion': self.find_pattern(
                r'(?:Duración|Duration|Tiempo)[\s:]*([0-9.]+[\s](?:horas|hours))',
                r'(?:Duración)[\s:]*([^\n]+)'
            ),
        }


def detect_document_type(pdf_file) -> Tuple[str, PDFExtractor]:
    """
    Detecta el tipo de documento y retorna el extractor apropiado
    
    Args:
        pdf_file: Archivo PDF
        
    Returns:
        Tupla (tipo, extractor_instance)
    """
    try:
        # Intentar ambos extractores
        calib_extractor = CertificadoCalibracionExtractor(pdf_file)
        mtto_extractor = InformeMantenimientoExtractor(pdf_file)
        
        calib_detected = calib_extractor.detect()
        mtto_detected = mtto_extractor.detect()
        
        # Si ambos detectan, priorizar basado en palabras clave
        if calib_detected and mtto_detected:
            # Contar keywords especícficos
            text = calib_extractor.full_text.lower()
            calib_score = sum(text.count(kw) for kw in ['presión', 'calibr', 'presion'])
            mtto_score = sum(text.count(kw) for kw in ['mantenim', 'servicio', 'revisión'])
            
            if calib_score > mtto_score:
                return 'calibracion', calib_extractor
            else:
                return 'mantenimiento', mtto_extractor
        
        elif calib_detected:
            return 'calibracion', calib_extractor
        elif mtto_detected:
            return 'mantenimiento', mtto_extractor
        else:
            return 'desconocido', calib_extractor  # Retorna uno por defecto
    
    except Exception as e:
        raise ValueError(f"Error detectando tipo de documento: {str(e)}")


def extract_data(pdf_file) -> Dict:
    """
    Extrae datos del PDF detectando automáticamente su tipo
    
    Args:
        pdf_file: Archivo PDF
        
    Returns:
        Diccionario con datos extraídos
    """
    try:
        doc_type, extractor = detect_document_type(pdf_file)
        data = extractor.extract()
        data['tipo_documento'] = doc_type
        return data
    except Exception as e:
        return {
            'tipo_documento': 'error',
            'error': str(e)
        }
