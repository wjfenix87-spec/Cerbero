from django.db import models

# Create your models here.
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=10)
    signos_y_síntomas = models.TextField()
    diagnóstico_presuntivo = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class SignosVitales(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='signos_vitales')
    presion_arterial = models.CharField(max_length=20)
    frecuencia_cardiaca = models.PositiveIntegerField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=1)
    saturacion_oxigeno = models.DecimalField(max_digits=4, decimal_places=1)
    frecuencia_respiratoria = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signos vitales de {self.paciente} - {self.fecha_hora}"

class RitmoCardiaco(models.Model):
    signos_vitales = models.ForeignKey(SignosVitales, on_delete=models.CASCADE, related_name='ritmo_cardiaco')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='ritmo_cardiaco')
    tipo_ritmo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ritmo cardiaco de {self.paciente} - {self.fecha_hora}"

class Monitorizacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    signos_vitales = models.OneToOneField('SignosVitales', on_delete=models.CASCADE, null=True, blank=True)
    ritmo_cardiaco = models.OneToOneField('RitmoCardiaco', on_delete=models.CASCADE, null=True, blank=True)
    tipo_ritmo = models.CharField(max_length=50, null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)
    spo2 = models.FloatField(null=True, blank=True)
    presion_arterial_sistolica = models.IntegerField(null=True, blank=True)
    presion_arterial_diastolica = models.IntegerField(null=True, blank=True)
    pam = models.FloatField(null=True, blank=True)
    temperatura = models.FloatField(null=True, blank=True)
    glasgow = models.IntegerField(null=True, blank=True)
    dolor_sedacion = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Monitoreo de {self.paciente} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"

class EscenarioClinico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    etapa_actual = models.ForeignKey('EtapaEscenario', on_delete=models.SET_NULL, null=True, blank=True, related_name='escenarios_actuales')
    modo_instructor = models.BooleanField(default=False, help_text="¿Permitir avance manual por docente?")
    # Puedes agregar más campos según lo que quieras mostrar

    def __str__(self):
        return self.nombre

class EtapaEscenario(models.Model):
    escenario = models.ForeignKey(EscenarioClinico, on_delete=models.CASCADE, related_name='etapas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField()
    # Puedes agregar campos para los valores de signos vitales en esta etapa
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)
    spo2 = models.FloatField(null=True, blank=True)
    presion_arterial_sistolica = models.IntegerField(null=True, blank=True)
    presion_arterial_diastolica = models.IntegerField(null=True, blank=True)
    pam = models.FloatField(null=True, blank=True)
    temperatura = models.FloatField(null=True, blank=True)
    glasgow = models.IntegerField(null=True, blank=True)
    dolor_sedacion = models.CharField(max_length=50, blank=True, null=True)
    duracion_segundos = models.PositiveIntegerField(null=True, blank=True, help_text="Duración de la etapa en segundos")
    avance_por_intervencion = models.BooleanField(default=False, help_text="¿Avanza por intervención?")

    def __str__(self):
        return f"{self.escenario.nombre} - {self.nombre}"

class Intervencion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='intervenciones')
    escenario = models.ForeignKey(EscenarioClinico, on_delete=models.CASCADE, related_name='intervenciones', null=True, blank=True)
    monitorizacion = models.ForeignKey(Monitorizacion, on_delete=models.CASCADE, related_name='intervenciones', null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50, choices=[
        ('evaluacion', 'Evaluación'),
        ('terapeutica', 'Terapéutica'),
        ('comunicacion', 'Comunicación/Escala'),
        ('confirmacion', 'Confirmación/Registro')
    ])
    descripcion = models.TextField()
    realizada_por = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.paciente} - {self.tipo} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"

class Evaluacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='evaluaciones')
    escenario = models.ForeignKey(EscenarioClinico, on_delete=models.CASCADE, related_name='evaluaciones', null=True, blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    duracion_segundos = models.PositiveIntegerField(null=True, blank=True)
    puntaje = models.PositiveIntegerField(default=0)
    checklist = models.TextField()  # Puedes usar JSONField si quieres guardar estructura
    errores = models.TextField()
    omisiones = models.TextField()
    competencias = models.TextField()
    debriefing = models.TextField()

    def __str__(self):
        return f"Evaluación de {self.paciente} en {self.escenario}"        