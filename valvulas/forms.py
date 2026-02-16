from django import forms
from valvulas.models import Valvula


class ValvulaEditarHojaVidaForm(forms.ModelForm):
    """
    Formulario para editar los datos de la Hoja de Vida de una válvula
    Los usuarios pueden modificar: ubicación, TAG, observaciones
    Los datos técnicos se cargan automáticamente desde los PDF
    """
    
    class Meta:
        model = Valvula
        fields = [
            'tag_localizacion',
            'ubicacion',
            'presion_set',
            'norma_aplicable',
            'observaciones',
            'estado',
        ]
        widgets = {
            'tag_localizacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: PSV-101, CV-45, etc',
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Línea A, Piso 2 - Sala de calderas',
            }),
            'presion_set': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 150 PSI',
                'readonly': 'readonly',
                'title': 'Este campo se actualiza automáticamente desde los documentos extraídos',
            }),
            'norma_aplicable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ASME I, ASME VIII',
                'readonly': 'readonly',
                'title': 'Este campo se actualiza automáticamente desde los documentos extraídos',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notas adicionales sobre la válvula, su mantenimiento, etc',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'tag_localizacion': 'TAG/Identificador',
            'ubicacion': 'Ubicación Física',
            'presion_set': 'Presión SET (Automático)',
            'norma_aplicable': 'Norma Aplicable (Automático)',
            'observaciones': 'Observaciones',
            'estado': 'Estado de la Válvula',
        }
        help_texts = {
            'tag_localizacion': 'Identificador único de la válvula en la planta',
            'ubicacion': 'Ubicación física donde está instalada la válvula',
            'observaciones': 'Cualquier información additional sobre mantenimiento o estado',
        }
