    
from django.urls import path
from . import views

urlpatterns = [
    path('crear_paciente/', views.crear_paciente, name='crear_paciente'),
    path('crear_signos_vitales/<int:paciente_id>/', views.crear_signos_vitales, name='crear_signos_vitales'),
    path('crear_ritmo_cardiaco/<int:signos_vitales_id>/', views.crear_ritmo_cardiaco, name='crear_ritmo_cardiaco'),
    path('monitorizacion/nueva/', views.crear_monitorizacion, name='crear_monitorizacion'),
    path('escenarios/nuevo/', views.crear_escenario, name='crear_escenario'),
    path('etapas/nueva/', views.crear_etapa, name='crear_etapa'),
    path('escenario/<int:escenario_id>/avanzar_etapa/', views.avanzar_etapa, name='avanzar_etapa'),
    path('monitorizaciones/', views.lista_monitorizaciones, name='lista_monitorizaciones'),
    path('escenarios/', views.lista_escenarios, name='lista_escenarios'),
    path('ritmos/', views.lista_ritmos_cardiacos, name='lista_ritmos_cardiacos'),
    path('intervenciones/nueva/', views.registrar_intervencion, name='registrar_intervencion'),
    path('intervenciones/', views.lista_intervenciones, name='lista_intervenciones'),
    path('intervenciones/filtrar/', views.filtrar_intervenciones, name='filtrar_intervenciones'),
    path('evaluaciones/nueva/', views.registrar_evaluacion, name='registrar_evaluacion'),
    path('evaluaciones/', views.lista_evaluaciones, name='lista_evaluaciones'),
    path('monitorizacion/<int:monitorizacion_id>/', views.detalle_monitorizacion, name='detalle_monitorizacion'),
    path('monitorizaciones/<int:monitorizacion_id>/', views.detalle_monitorizacion, name='detalle_monitorizacion'),
]
