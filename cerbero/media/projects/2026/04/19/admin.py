# Registrar todos los modelos en el admin
from django.contrib import admin
from .models import Paciente, SignosVitales, RitmoCardiaco, Monitorizacion, EscenarioClinico, EtapaEscenario, Intervencion, Evaluacion

admin.site.register(Paciente)
admin.site.register(SignosVitales)
admin.site.register(RitmoCardiaco)
admin.site.register(Monitorizacion)
admin.site.register(EscenarioClinico)
admin.site.register(EtapaEscenario)
admin.site.register(Intervencion)
admin.site.register(Evaluacion)
# Register your models here.
