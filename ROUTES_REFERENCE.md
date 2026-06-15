# 🚀 Rutas Disponibles - WebCerbero

## 📍 URLs del Proyecto

### Páginas Principales

| Ruta | Nombre | Vista | Template | Descripción |
|------|--------|-------|----------|-------------|
| `/` | `home` | `core_views.home` | `core/home.html` | **Página principal** del proyecto |
| `/index/` | `index` | `core_views.index` | `core/index.html` | **Página de origen** - Origen, Servidor e IAs |
| `/sesion/` | `sesion` | `core_views.sesion` | `core/sesion.html` | **Página de login** - Acceso al sistema |

### APIs

| Ruta | Descripción |
|------|-------------|
| `/api/auth/register/` | Registro de usuarios |
| `/api/auth/login/` | Login de usuarios |
| `/api/auth/me/` | Info usuario actual |
| `/api/auth/logout/` | Cerrar sesión |
| `/api/auth/profile/` | Perfil del usuario |
| `/api/health/` | Health check |
| `/api/projects/` | Endpoints de proyectos |

### Proyectos

| Ruta | Descripción |
|------|-------------|
| `/p/<slug>/` | Ver proyecto público |
| `/p/<slug>/info/` | Info del proyecto (JSON) |
| `/p/<slug>/update/` | Actualizar proyecto |
| `/p/<slug>/delete/` | Eliminar proyecto |
| `/p/api/upload/` | Subir archivos |
| `/p/api/upload-folder/` | Subir carpeta |
| `/p/api/upload-zip/` | Subir ZIP |
| `/p/api/my-projects/` | Mis proyectos |
| `/p/download/<slug>/` | Descargar para IA |

### Guías de Upload

| Ruta | Descripción |
|------|-------------|
| `/upload-guide/django/` | Guía Django |
| `/upload-guide/flutter/` | Guía Flutter |
| `/upload-guide/react/` | Guía React |
| `/upload-guide/angular/` | Guía Angular |
| `/upload-guide/vue/` | Guía Vue.js |
| `/upload-guide/node/` | Guía Node.js |
| `/upload-guide/spring/` | Guía Spring Boot |
| `/upload-guide/laravel/` | Guía Laravel |
| `/upload-guide/html/` | Guía HTML/CSS/JS |

### Otras Páginas

| Ruta | Template | Descripción |
|------|----------|-------------|
| `/docs/` | `core/docs.html` | Documentación |
| `/terms/` | `core/terms.html` | Términos y condiciones |
| `/privacy/` | `core/privacy.html` | Política de privacidad |
| `/cookies/` | `core/cookies.html` | Política de cookies |
| `/admin/` | Admin | Panel de administración Django |

---

## 🖼️ Imágenes Disponibles

Todas las imágenes están en: `cerbero/static/assets/`

| Archivo | Tamaño | Uso |
|---------|--------|-----|
| `1.jpg` | 92.7KB | Fondo principal |
| `2.png` | 13.1MB | Logo pequeño (esquina) |
| `fondo.png` | 2.1MB | Fondo hero |
| `logo.png` | 237.3KB | Logo principal |
| `logo1.png` | 13.1MB | Logo alternativo |

### Uso en Templates

```html
{% load static %}

<!-- En index.html -->
<img src="{% static 'assets/fondo.png' %}" alt="Data flows" />
<img src="{% static 'assets/logo.png' %}" alt="CERBERO Logo" />

<!-- En sesion.html -->
<img src="{% static 'assets/1.jpg' %}" alt="Sistema Cerbero" />
<img src="{% static 'assets/2.png' %}" alt="CERBERO" />
```

---

## 🔗 Navegación entre Páginas

### Desde index.html
```html
<!-- Ir al home -->
<a href="{% url 'home' %}">Ir al Home</a>

<!-- Ir a sesión/login -->
<a href="{% url 'sesion' %}">Iniciar Sesión</a>
```

### Desde sesion.html
```html
<!-- Volver al index -->
<a href="{% url 'index' %}">Volver</a>

<!-- Ir al home después de login -->
window.location.href = "{% url 'home' %}";
```

### Desde home.html
```html
<!-- Ir al index -->
<a href="{% url 'index' %}">Origen</a>

<!-- Ir a sesión -->
<a href="{% url 'sesion' %}">Ingresar</a>
```

---

## 🧪 Probar Localmente

### 1. Ejecutar servidor
```bash
cd "d:\Git GitHub\WebCerbero\cerbero"
python manage.py runserver
```

### 2. Acceder a las páginas

- **Home:** http://localhost:8000/
- **Index:** http://localhost:8000/index/
- **Sesion:** http://localhost:8000/sesion/
- **Admin:** http://localhost:8000/admin/
- **Docs:** http://localhost:8000/docs/
- **Health Check:** http://localhost:8000/api/health/

---

## 📁 Estructura de Templates

```
cerbero/templates/core/
├── home.html          ← Página principal (/)
├── index.html         ← Página de origen (/index/)
├── sesion.html        ← Login (/sesion/)
├── project.html       ← Vista de proyecto
├── upload_guide.html  ← Guías de upload
├── profile.html       ← Perfil usuario
├── docs.html          ← Documentación
├── terms.html         ← Términos
├── privacy.html       ← Privacidad
├── cookies.html       ← Cookies
└── expired.html       ← Proyecto expirado
```

---

## ⚙️ Configuración de Static Files

### settings.py
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# En desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Recopilar static files (producción)
```bash
python manage.py collectstatic --noinput
```

---

## 🎯 Flujo de Usuario Típico

1. **Usuario llega** → `/index/` (Página de origen)
2. **Click en ingresar** → `/sesion/` (Login/Registro)
3. **Login exitoso** → Redirige a `/` (Home principal)
4. **Sube proyecto** → `/upload-guide/<framework>/`
5. **Ve proyecto** → `/p/<slug>/`

---

## 🔧 Troubleshooting

### Imágenes no cargan
```bash
# Verificar que static files están configurados
python manage.py findstatic assets/logo.png

# Recopilar static files
python manage.py collectstatic --noinput
```

### Ruta no encontrada (404)
```bash
# Verificar URLs configuradas
python manage.py show_urls  # Si tiene django-extensions
```

### Error 500
```bash
# Verificar logs
tail -f error.log

# Check del sistema
python manage.py check
```

---

## ✅ Checklist

- [x] `/index/` - Vista creada y URL configurada
- [x] `/sesion/` - Vista creada y URL configurada
- [x] Imágenes en `static/assets/` accesibles
- [x] Templates usan `{% load static %}` correctamente
- [x] URLs con nombres (`name='index'`, `name='sesion'`)
- [x] System check sin errores

---

**¡Todas las rutas están configuradas y listas! 🚀**
