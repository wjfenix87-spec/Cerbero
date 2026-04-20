from django.shortcuts import render, redirect
from .models import Paciente, SignosVitales, RitmoCardiaco, Monitorizacion, Evaluacion, Intervencion
from .forms import PacienteForm, SignosVitalesForm, RitmoCardiacoForm
from .forms import MonitorizacionForm, EscenarioClinicoForm, EtapaEscenarioForm
from .utils import evaluar_alarmas
from .models import EscenarioClinico
from .forms import IntervencionForm



# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def crear_paciente(request):
    from .forms import PacienteForm
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return redirect('crear_signos_vitales', paciente_id=paciente.id)
    else:
        form = PacienteForm()
    return render(request, 'crear_paciente.html', {'form': form})

def crear_signos_vitales(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    if request.method == 'POST':
        presion_arterial = request.POST['presion_arterial']
        frecuencia_cardiaca = request.POST['frecuencia_cardiaca']
        temperatura = request.POST['temperatura']
        saturacion_oxigeno = request.POST['saturacion_oxigeno']
        frecuencia_respiratoria = request.POST['frecuencia_respiratoria']

        signos_vitales = SignosVitales.objects.create(
            paciente=paciente,
            presion_arterial=presion_arterial,
            frecuencia_cardiaca=frecuencia_cardiaca,
            temperatura=temperatura,
            saturacion_oxigeno=saturacion_oxigeno,
            frecuencia_respiratoria=frecuencia_respiratoria
        )
        # Extraer presión sistólica si el formato es '120/80'
        pas = None
        if '/' in presion_arterial:
            try:
                pas = int(presion_arterial.split('/')[0])
            except Exception:
                pas = None
        elif presion_arterial.isdigit():
            pas = int(presion_arterial)
        # Crear monitorización asociada
        Monitorizacion.objects.create(
            paciente=paciente,
            signos_vitales=signos_vitales,
            frecuencia_cardiaca=frecuencia_cardiaca,
            frecuencia_respiratoria=frecuencia_respiratoria,
            spo2=saturacion_oxigeno,
            presion_arterial_sistolica=pas,
            temperatura=temperatura
        )
        return redirect('lista_monitorizaciones')
    return render(request, 'crear_signos_vitales.html', {'paciente': paciente})

def crear_ritmo_cardiaco(request, signos_vitales_id):
    signos_vitales = SignosVitales.objects.get(id=signos_vitales_id)
    paciente = signos_vitales.paciente
    if request.method == 'POST':
        tipo_ritmo = request.POST.get('tipo_ritmo')
        frecuencia = request.POST.get('frecuencia')
        descripcion = request.POST.get('descripcion')
        ritmo_cardiaco = RitmoCardiaco.objects.create(
            paciente=paciente,
            signos_vitales=signos_vitales,
            tipo_ritmo=tipo_ritmo,
            descripcion=descripcion
        )
        return redirect('lista_ritmos_cardiacos')  # <-- Cambia aquí el redirect
    signos_vitales_list = SignosVitales.objects.filter(paciente=paciente)
    return render(request, 'crear_ritmo_cardiaco.html', {
        'paciente': paciente,
        'signos_vitales_list': signos_vitales_list,
        'signos_vitales_id': signos_vitales_id
    })

def lista_ritmos_cardiacos(request):
    ritmos = RitmoCardiaco.objects.all()
    return render(request, 'lista_ritmos_cardiacos.html', {'ritmos': ritmos})


def crear_monitorizacion(request):
    if request.method == 'POST':
        form = MonitorizacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_monitorizaciones')  # Cambia esto por la URL que desees
    else:
        form = MonitorizacionForm()
    return render(request, 'crear_monitorizacion.html', {'form': form})


def crear_escenario(request):
    if request.method == 'POST':
        form = EscenarioClinicoForm(request.POST)
        if form.is_valid():
            escenario = form.save()
            # Redirigir a crear_etapa, pasando el id del escenario
            return redirect('crear_etapa')
    else:
        form = EscenarioClinicoForm()
    return render(request, 'crear_escenario.html', {'form': form})

def crear_etapa(request):
    if request.method == 'POST':
        form = EtapaEscenarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_escenarios')
    else:
        form = EtapaEscenarioForm()
    return render(request, 'crear_etapa.html', {'form': form})


def lista_monitorizaciones(request):
    monitorizaciones = Monitorizacion.objects.all()
    monitorizaciones_alarmas = []
    for m in monitorizaciones:
        signos = {
            'frecuencia_cardiaca': m.frecuencia_cardiaca,
            'frecuencia_respiratoria': m.frecuencia_respiratoria,
            'spo2': m.spo2,
            'presion_arterial_sistolica': m.presion_arterial_sistolica,
            'temperatura': m.temperatura,
        }
        alarmas = evaluar_alarmas(signos)
        monitorizaciones_alarmas.append((m, alarmas))
    return render(request, 'lista_monitorizaciones.html', {'monitorizaciones_alarmas': monitorizaciones_alarmas})


def detalle_monitorizacion(request, monitorizacion_id):
    monitorizacion = Monitorizacion.objects.get(id=monitorizacion_id)
    # Calcular alarmas usando la función utilitaria
    signos = {
        'frecuencia_cardiaca': monitorizacion.frecuencia_cardiaca,
        'frecuencia_respiratoria': monitorizacion.frecuencia_respiratoria,
        'spo2': monitorizacion.spo2,
        'presion_arterial_sistolica': monitorizacion.presion_arterial_sistolica,
        'temperatura': monitorizacion.temperatura
    }
    alarmas = evaluar_alarmas(signos)
    # Pasar alarmas al template
    return render(request, 'detalle_monitorizacion.html', {
        'monitorizacion': monitorizacion,
        'alarmas': alarmas
    })


def lista_escenarios(request):
    escenarios = EscenarioClinico.objects.prefetch_related('etapas').all()
    return render(request, 'lista_escenarios.html', {'escenarios': escenarios})

def registrar_intervencion(request):
    if request.method == 'POST':
        form = IntervencionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_intervenciones')
    else:
        form = IntervencionForm()
    return render(request, 'registrar_intervencion.html', {'form': form})

def lista_intervenciones(request):
    intervenciones = Intervencion.objects.select_related('paciente', 'escenario', 'monitorizacion').all()
    return render(request, 'lista_intervenciones.html', {'intervenciones': intervenciones})

from .models import Paciente, EscenarioClinico, Monitorizacion, Intervencion

def filtrar_intervenciones(request):
    pacientes = Paciente.objects.all()
    escenarios = EscenarioClinico.objects.all()
    monitorizaciones = Monitorizacion.objects.all()

    paciente_id = request.GET.get('paciente')
    escenario_id = request.GET.get('escenario')
    monitorizacion_id = request.GET.get('monitorizacion')

    intervenciones = Intervencion.objects.all()

    if paciente_id:
        intervenciones = intervenciones.filter(paciente_id=paciente_id)
    if escenario_id:
        intervenciones = intervenciones.filter(escenario_id=escenario_id)
    if monitorizacion_id:
        intervenciones = intervenciones.filter(monitorizacion_id=monitorizacion_id)

    return render(request, 'filtrar_intervenciones.html', {
        'intervenciones': intervenciones,
        'pacientes': pacientes,
        'escenarios': escenarios,
        'monitorizaciones': monitorizaciones,
        'paciente_id': paciente_id,
        'escenario_id': escenario_id,
        'monitorizacion_id': monitorizacion_id,
    })

def registrar_evaluacion(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_evaluaciones')
    else:
        form = EvaluacionForm()
    return render(request, 'registrar_evaluacion.html', {'form': form})

def lista_evaluaciones(request):
    evaluaciones = Evaluacion.objects.all()
    return render(request, 'lista_evaluaciones.html', {'evaluaciones': evaluaciones})    

def avanzar_etapa(request, escenario_id):
    escenario = EscenarioClinico.objects.get(id=escenario_id)
    etapas = escenario.etapas.order_by('orden')
    actual = escenario.etapa_actual
    siguiente = None
    if actual:
        for etapa in etapas:
            if etapa.orden > actual.orden:
                siguiente = etapa
                break
    else:
        if etapas.exists():
            siguiente = etapas.first()
    if siguiente:
        escenario.etapa_actual = siguiente
        escenario.save()
    return redirect('detalle_escenario', escenario_id=escenario.id)