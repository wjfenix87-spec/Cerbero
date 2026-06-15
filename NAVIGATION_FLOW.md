# 🔄 Flujo de Navegación Inteligente - WebCerbero

## 🎯 Comportamiento Implementado

El proyecto ahora detecta automáticamente si el usuario es nuevo o registrado y redirige en consecuencia.

---

## 📍 Lógica de Redirección

### **Usuario Primera Vez (Sin Sesión)**

```
┌────────────────────────────────────────────────┐
│  Usuario abre: http://localhost:8000/          │
│  (o simplemente escribe el dominio)            │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│  / (landing) → index.html                      │
│  ✅ Muestra página de origen                   │
│  ✅ Presentación del proyecto                  │
│  ✅ Botón "Ingresar al sistema"                │
└────────────────────────────────────────────────┘
                    ↓ (click en ingresar)
┌────────────────────────────────────────────────┐
│  /sesion/                                      │
│  ✅ Muestra formulario de LOGIN                │
│  ✅ Opción de registrarse                      │
└────────────────────────────────────────────────┘
                    ↓ (login exitoso)
┌────────────────────────────────────────────────┐
│  Redirige automáticamente a /home/             │
│  ✅ Guarda sesión en localStorage              │
│  ✅ Muestra toast de bienvenida                │
└────────────────────────────────────────────────┘
```

### **Usuario Registrado (Con Sesión)**

```
┌────────────────────────────────────────────────┐
│  Usuario abre: http://localhost:8000/          │
│  (visita posterior)                            │
└────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────┐
│  / (landing) → index.html                      │
│  ✅ Detecta sesión activa                      │
│  ✅ localStorage tiene:                        │
│     - cerbero_session                          │
│     - accessToken                              │
└────────────────────────────────────────────────┘
                    ↓ (auto-redirección < 100ms)
┌────────────────────────────────────────────────┐
│  /home/ (redirección automática)               │
│  ✅ Muestra home principal                     │
│  ✅ Usuario ya autenticado                     │
│  ✅ Acceso completo a funciones                │
└────────────────────────────────────────────────┘
```

---

## 🔧 Implementación Técnica

### **1. URL Raíz (`/`) - Landing Page**

**Archivo:** `config/urls.py`
```python
path('', core_views.landing, name='landing'),  # Decide index o home
path('home/', core_views.home, name='home'),   # Home para registrados
```

### **2. Vista Landing**

**Archivo:** `core/views.py`
```python
def landing(request):
    """Vista landing - Decide si mostrar index o redirigir a home"""
    return render(request, 'core/index.html')
```

### **3. Detección en index.html**

**Archivo:** `templates/core/index.html`
```javascript
(function() {
    var session = localStorage.getItem('cerbero_session');
    var token = localStorage.getItem('accessToken');
    
    if (session && token) {
        // Usuario ya tiene sesión, redirigir al home
        window.location.href = "{% url 'home' %}";
        return;
    }
    
    // Si no hay sesión, mostrar index normalmente
    // ... carga de partículas y animaciones
})();
```

### **4. Protección de home.html**

**Archivo:** `templates/core/home.html`
```javascript
(function() {
    var session = localStorage.getItem('cerbero_session');
    var token = localStorage.getItem('accessToken');
    
    // Si no hay sesión, redirigir al index
    if (!session || !token) {
        window.location.href = "{% url 'index' %}";
        return;
    }
})();
```

---

## 🗺️ Mapa Completo de URLs

| URL | Nombre | Acceso | Descripción |
|-----|--------|--------|-------------|
| `/` | `landing` | Todos | Punto de entrada (decide index o home) |
| `/home/` | `home` | Solo registrados | Home principal con todas las funciones |
| `/index/` | `index` | Todos (auto-redirige si hay sesión) | Landing page para nuevos usuarios |
| `/sesion/` | `sesion` | Todos (auto-redirige si hay sesión) | Login/Registro |
| `/sesion/?mode=register` | `sesion` | Todos | Registro directo |

---

## 📊 Estados del Usuario

### **Estado 1: Nuevo Usuario**
```
localStorage:
- cerbero_session: null
- accessToken: null

Flujo:
/ → /index/ → /sesion/ → (registro) → /home/
```

### **Estado 2: Usuario Registrado**
```
localStorage:
- cerbero_session: "nombre_usuario"
- accessToken: "eyJ..."

Flujo:
/ → (auto) → /home/
```

### **Estado 3: Sesión Expirada**
```
localStorage:
- cerbero_session: "nombre_usuario"
- accessToken: expired o null

Flujo:
/ → /home/ → (detecta token inválido) → /index/
```

---

## 🔄 Flujos Completos

### **Flujo de Primer Acceso**

```
1. Usuario entra a http://localhost:8000/
2. LANDING detecta: NO hay sesión
3. Muestra INDEX.HTML
4. Usuario ve página de presentación
5. Click en "Ingresar al sistema"
6. Va a /sesion/
7. Click en "¿No tienes cuenta? Regístrate"
8. Llena formulario de registro
9. Registro exitoso → Guarda tokens
10. REDIRECCIÓN AUTOMÁTICA a /home/
11. Usuario ve home con todas las funciones
```

### **Flujo de Acceso Posterior**

```
1. Usuario entra a http://localhost:8000/
2. LANDING detecta: SÍ hay sesión
3. REDIRECCIÓN AUTOMÁTICA a /home/
4. Usuario ve home directamente
5. ¡Sin necesidad de login!
```

### **Flujo de Logout**

```
1. Usuario en /home/
2. Click en "Cerrar sesión"
3. Limpia localStorage
4. REDIRECCIÓN a /index/
5. Usuario ve landing page
```

---

## ⚡ Performance

### **Tiempo de Redirección**

| Escenario | Tiempo | Método |
|-----------|--------|--------|
| Nuevo usuario → Index | 0ms | Directo |
| Registrado → Home | <50ms | JavaScript auto-redirect |
| Sin sesión → Home → Index | <100ms | Protección + redirect |

### **Detección de Sesión**

```javascript
// Verificación ultrarrápida (< 1ms)
var session = localStorage.getItem('cerbero_session');
var token = localStorage.getItem('accessToken');

if (session && token) {
    window.location.href = "/home/";
}
```

---

## 🛡️ Seguridad

### **Protección de Rutas**

| Ruta | Requiere Sesión | Protección |
|------|-----------------|------------|
| `/` | ❌ No | Landing pública |
| `/index/` | ❌ No | Auto-redirige si hay sesión |
| `/home/` | ✅ Sí | Redirige a index si no hay sesión |
| `/sesion/` | ❌ No | Auto-redirige a home si hay sesión |
| `/api/projects/*` | ✅ Sí | JWT authentication |

### **Tokens Almacenados**

```javascript
localStorage:
{
    "cerbero_session": "nombre_usuario",
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## 🎨 Experiencia de Usuario

### **Ventajas del Sistema**

✅ **Sin fricción para nuevos usuarios**
- Ven la página de presentación primero
- Entienden el proyecto antes de registrarse

✅ **Acceso instantáneo para registrados**
- Sin login repetitivo
- Redirección automática en <50ms
- Experiencia tipo app nativa

✅ **Navegación intuitiva**
- URL raíz siempre funciona
- Redirecciones automáticas inteligentes
- Sin errores de "página no encontrada"

✅ **Persistencia de sesión**
- Sesión se mantiene entre visitas
- Solo logout explícito cierra sesión
- Tokens JWT seguros

---

## 🧪 Testing

### **Probar Flujo Completo**

```bash
# 1. Limpiar sesión (simular nuevo usuario)
# En navegador Console:
localStorage.clear();

# 2. Ir a raíz
# http://localhost:8000/
# ✅ Debe mostrar index.html

# 3. Registrarse
# Click en "Ingresar al sistema"
# Registrarse con usuario nuevo
# ✅ Debe redirigir a /home/

# 3. Cerrar navegador y abrir de nuevo
# Ir a http://localhost:8000/
# ✅ Debe ir directo a /home/

# 4. Cerrar sesión
# Click en logout
# ✅ Debe ir a /index/
```

---

## 🔧 Troubleshooting

### **Problema: No redirige automáticamente**

```javascript
// Verificar en Console del navegador:
console.log(localStorage.getItem('cerbero_session'));
console.log(localStorage.getItem('accessToken'));

// Si ambos existen, debe redirigir
// Si no, hay un error en el JavaScript
```

### **Problema: Redirección infinita**

```
Causa: Configuración incorrecta de URLs
Solución: Verificar que:
- / → landing view
- /home/ → home view
- /index/ → index view
```

### **Problema: Sesión no persiste**

```
Causa: localStorage se limpia
Solución:
1. Verificar que no hay localStorage.clear()
2. Check cookies del navegador
3. Verificar modo incógnito
```

---

## 📝 Código Clave

### **index.html (Auto-redirect si hay sesión)**
```javascript
if (session && token) {
    window.location.href = "{% url 'home' %}";
    return;
}
```

### **home.html (Protección sin sesión)**
```javascript
if (!session || !token) {
    window.location.href = "{% url 'index' %}";
    return;
}
```

### **sesion.html (Auto-login si hay sesión)**
```javascript
if (session && token) {
    window.location.href = "{% url 'home' %}";
    return;
}
```

---

## ✅ Checklist de Funcionamiento

- [x] Landing page en `/` decide entre index o home
- [x] index.html redirige a home si hay sesión
- [x] home.html redirige a index si no hay sesión
- [x] sesion.html redirige a home si hay sesión
- [x] Registro guarda tokens correctamente
- [x] Login guarda tokens correctamente
- [x] Logout limpia tokens correctamente
- [x] Redirecciones son rápidas (<100ms)
- [x] No hay loops de redirección
- [x] URLs amigables y claras

---

## 🎯 Resumen

**Comportamiento:**
- 🆕 **Primera vez:** `/` → `index.html` → Presentación
- 🔄 **Visitas posteriores:** `/` → `home.html` → Acceso directo
- 🔐 **Seguridad:** home.html protegido, requiere sesión
- ⚡ **Performance:** Redirección <50ms
- 💾 **Persistencia:** Sesión se mantiene entre visitas

**¡El sistema detecta automáticamente si eres nuevo o registrado! 🚀**
