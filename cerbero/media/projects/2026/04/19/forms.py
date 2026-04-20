from django import forms
from .models import Paciente, SignosVitales, RitmoCardiaco, Monitorizacion

class PacienteForm(forms.ModelForm):
    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is not None and edad < 18:
            raise forms.ValidationError('Solo se permiten pacientes adultos (18 años o más).')
        return edad

    class Meta:
        model = Paciente
        fields = ['nombre', 'apellidos', 'edad', 'sexo', 'signos_y_síntomas', 'diagnóstico_presuntivo']
        error_messages = {
            'nombre': {'required': 'Este campo es obligatorio.'},
            'apellidos': {'required': 'Este campo es obligatorio.'},
            'edad': {'required': 'Este campo es obligatorio.'},
            'sexo': {'required': 'Este campo es obligatorio.'},
            'signos_y_síntomas': {'required': 'Este campo es obligatorio.'},
            'diagnóstico_presuntivo': {'required': 'Este campo es obligatorio.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['rows'] = 5
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class SignosVitalesForm(forms.ModelForm):
    class Meta:
        model = SignosVitales
        fields = ['paciente', 'presion_arterial', 'frecuencia_cardiaca', 'temperatura', 'saturacion_oxigeno', 'frecuencia_respiratoria']

class RitmoCardiacoForm(forms.ModelForm):
    class Meta:
        model = RitmoCardiaco
        fields = ['signos_vitales', 'paciente', 'tipo_ritmo', 'descripcion']

class MonitorizacionForm(forms.ModelForm):
    class Meta:
        model = Monitorizacion
        fields = [
            'paciente',
            'ritmo_cardiaco',
            'frecuencia_cardiaca',
            'frecuencia_respiratoria',
            'spo2',
            'presion_arterial_sistolica',
            'presion_arterial_diastolica',
            'pam',
            'temperatura',
            'glasgow',
            'dolor_sedacion',
        ]
from .models import EscenarioClinico, EtapaEscenario

class EscenarioClinicoForm(forms.ModelForm):
    class Meta:
        model = EscenarioClinico
        fields = ['nombre', 'descripcion']

class EtapaEscenarioForm(forms.ModelForm):
    class Meta:
        model = EtapaEscenario
        fields = [
            'escenario',
            'nombre',
            'descripcion',
            'orden',
            'frecuencia_cardiaca',
            'frecuencia_respiratoria',
            'spo2',
            'presion_arterial_sistolica',
            'presion_arterial_diastolica',
            'pam',
            'temperatura',
            'glasgow',
            'dolor_sedacion',
        ]

from .models import Intervencion

class IntervencionForm(forms.ModelForm):
    class Meta:
        model = Intervencion
        fields = ['paciente', 'escenario', 'monitorizacion', 'tipo', 'descripcion', 'realizada_por']

from .models import Evaluacion

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = [
            'paciente', 'escenario', 'fecha_inicio', 'fecha_fin', 'duracion_segundos',
            'puntaje', 'checklist', 'errores', 'omisiones', 'competencias', 'debriefing'
        ]