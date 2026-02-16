from django import forms
from servicios.models import Certificado, Documento, Servicio


class CertificadoForm(forms.ModelForm):
    """
    Formulario para crear/editar certificados
    Permite al comercial subir archivos PDF
    """
    
    class Meta:
        model = Certificado
        fields = [
            'tipo_certificado',
            'numero_certificado', 
            'fecha_emision',
            'fecha_vencimiento',
            'archivo_pdf',
            'presion_inicial',
            'presion_final',
            'temperatura',
            'resultado',
            'notas_calibracion',
            'laboratorio',
            'tecnico_responsable'
        ]
        widgets = {
            'tipo_certificado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'numero_certificado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: CERT-2026-001'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'archivo_pdf': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            }),
            'presion_inicial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 50 PSI'
            }),
            'presion_final': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 50 PSI'
            }),
            'temperatura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 25°C'
            }),
            'resultado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: APROBADO/RECHAZADO'
            }),
            'notas_calibracion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales del proceso de calibración'
            }),
            'laboratorio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del laboratorio'
            }),
            'tecnico_responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del técnico'
            }),
        }

    def clean_archivo_pdf(self):
        """Valida que el archivo sea PDF y no exceda 10MB"""
        archivo = self.cleaned_data.get('archivo_pdf')
        if archivo:
            # Verificar tamaño
            if archivo.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('El archivo no puede exceder 10MB')
            
            # Verificar extensión
            if not archivo.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Solo se aceptan archivos PDF')
        
        return archivo


class DocumentoForm(forms.ModelForm):
    """
    Formulario para crear/editar documentos (certificados e informes)
    Permite al comercial subir archivos PDF con detección automática de tipo
    """
    
    class Meta:
        model = Documento
        fields = [
            'archivo_pdf',
            'servicio',
            'fecha_documento',
            'fecha_vencimiento',
        ]
        widgets = {
            'archivo_pdf': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-select',
            }),
            'fecha_documento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def clean_archivo_pdf(self):
        """Valida que el archivo sea PDF y no exceda 10MB"""
        archivo = self.cleaned_data.get('archivo_pdf')
        if archivo:
            # Verificar tamaño
            if archivo.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('El archivo no puede exceder 10MB')
            
            # Verificar extensión
            if not archivo.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Solo se aceptan archivos PDF')
        
        return archivo


class ServicioConCertificadoForm(forms.ModelForm):
    """
    Formulario para crear un servicio con certificado en un solo paso
    """
    
    class Meta:
        model = Servicio
        fields = [
            'valvula',
            'tipo_servicio',
            'fecha_servicio',
            'descripcion',
            'observaciones',
        ]
        widgets = {
            'valvula': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tipo_servicio': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_servicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del servicio realizado'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            }),
        }
