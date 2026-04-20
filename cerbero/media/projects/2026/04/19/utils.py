def evaluar_alarmas(signos):
    alarmas = {}

    # Frecuencia cardíaca (FC)
    fc = signos.get('frecuencia_cardiaca')
    if fc is not None:
        if fc < 40 or fc > 150:
            alarmas['frecuencia_cardiaca'] = 'crítica'
        elif fc < 50 or fc > 120:
            alarmas['frecuencia_cardiaca'] = 'alta'
        elif fc < 60 or fc > 100:
            alarmas['frecuencia_cardiaca'] = 'media'
        else:
            alarmas['frecuencia_cardiaca'] = 'normal'

    # Frecuencia respiratoria (FR)
    fr = signos.get('frecuencia_respiratoria')
    if fr is not None:
        if fr > 35 or fr < 8:
            alarmas['frecuencia_respiratoria'] = 'crítica'
        elif fr > 24 or fr < 10:
            alarmas['frecuencia_respiratoria'] = 'media'
        elif 21 <= fr <= 24 or 10 <= fr <= 11:
            alarmas['frecuencia_respiratoria'] = 'baja'
        else:
            alarmas['frecuencia_respiratoria'] = 'normal'

    # Saturación de oxígeno (SpO2)
    spo2 = signos.get('spo2')
    if spo2 is not None:
        if spo2 < 85:
            alarmas['spo2'] = 'crítica'
        elif spo2 < 90:
            alarmas['spo2'] = 'media'
        elif spo2 < 94:
            alarmas['spo2'] = 'baja'
        else:
            alarmas['spo2'] = 'normal'

    # Presión arterial sistólica (PAS)
    pas = signos.get('presion_arterial_sistolica')
    if pas is not None:
        if pas < 80:
            alarmas['presion_arterial_sistolica'] = 'crítica'
        elif pas < 90 or pas >= 160:
            alarmas['presion_arterial_sistolica'] = 'amarilla'
        elif pas < 100 or pas >= 140:
            alarmas['presion_arterial_sistolica'] = 'verde'
        else:
            alarmas['presion_arterial_sistolica'] = 'normal'

    # Temperatura
    temp = signos.get('temperatura')
    if temp is not None:
        if temp > 39.0 or temp < 35.0:
            alarmas['temperatura'] = 'crítica'
        elif temp > 38.0 or temp < 35.5:
            alarmas['temperatura'] = 'alta'
        elif temp > 37.5 or temp < 35.9:
            alarmas['temperatura'] = 'media'
        else:
            alarmas['temperatura'] = 'normal'

    return alarmas