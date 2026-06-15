# 🚀 Guía de Despliegue - WebCerbero en Producción

## Pre-requisitos

- Cuenta en Render (u otro hosting)
- Base de datos PostgreSQL (Render proporciona una gratuita)
- Dominio configurado (opcional)

---

## 1️⃣ **Configuración de Variables de Entorno en Render**

### Variables Obligatorias

```env
DEBUG=False
SECRET_KEY=<generar-nueva-clave-segura>
ALLOWED_HOSTS=cerbero.onrender.com,localhost
CORS_ALLOWED_ORIGINS=https://cerbero.onrender.com
CSRF_TRUSTED_ORIGINS=https://cerbero.onrender.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
DJANGO_LOG_LEVEL=WARNING
```

### Generar Nueva SECRET_KEY

Ejecuta localmente:
```bash
cd cerbero
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia la clave generada y pégala en Render.

---

## 2️⃣ **Configuración de Base de Datos PostgreSQL en Render**

1. Ve a Render Dashboard
2. Crea nuevo **PostgreSQL** database
3. Copia la **Internal Database URL**
4. Pega en la variable `DATABASE_URL`

Formato:
```
postgresql://username:password@hostname:5432/database_name
```

---

## 3️⃣ **Configuración del Servicio en Render**

### Build Settings

- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command:** `gunicorn config.wsgi:application`

### Environment

- **Python Version:** 3.11+
- **Region:** Oregon (us-west-2) o la más cercana

---

## 4️⃣ **Migraciones en Producción**

### Automático (Recomendado)
Agregar en Render Build Command:
```bash
python manage.py migrate
```

### Manual (Si es necesario)
```bash
# Acceder al servidor vía SSH
render.com login

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

---

## 5️⃣ **Static Files Configuration**

### settings.py (Ya configurado)
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise para servir static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Después de SecurityMiddleware
    # ...
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Collectstatic
```bash
python manage.py collectstatic --noinput
```

---

## 6️⃣ **Configuración de Seguridad**

### HTTPS Forzado
Ya configurado en `settings.py`:
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

### CSRF Protection
```python
CSRF_TRUSTED_ORIGINS = ['https://cerbero.onrender.com']
```

---

## 7️⃣ **Monitoreo y Logs**

### Logs en Render
- Ve a **Logs** en el dashboard de Render
- Filtra por nivel: ERROR, WARNING, INFO

### Error Tracking
Los errores se guardan en `error.log` (no commitear a Git)

### Health Check
Endpoint disponible: `/api/health/`

Response:
```json
{
    "status": "ok",
    "message": "Cerbero API funcionando 🐕",
    "version": "1.0.0"
}
```

---

## 8️⃣ **Performance Optimization**

### Database Connection Pooling
Ya configurado en `settings.py`:
```python
DATABASES['default'] = dj_database_url.config(
    default=os.getenv('DATABASE_URL'),
    conn_max_age=600,  # Connection pooling
    conn_health_checks=True,
)
```

### Gunicorn Configuration
Crear archivo `gunicorn.conf.py`:
```python
bind = "0.0.0.0:$PORT"
workers = 3
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

---

## 9️⃣ **Backup de Base de Datos**

### Automático (Render Free Tier)
- Render hace backups automáticos cada día
- Retención: 7 días

### Manual
```bash
# Exportar base de datos
pg_dump -h hostname -U username dbname > backup.sql

# Importar base de datos
psql -h hostname -U username dbname < backup.sql
```

---

## 🔟 **Checklist Pre-Despliegue**

### Seguridad
- [ ] `DEBUG=False` configurado
- [ ] `SECRET_KEY` nueva generada
- [ ] `ALLOWED_HOSTS` restringido
- [ ] `CORS_ALLOWED_ORIGINS` configurado
- [ ] HTTPS habilitado
- [ ] CSRF tokens configurados

### Base de Datos
- [ ] PostgreSQL creado en Render
- [ ] `DATABASE_URL` configurado
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado

### Static Files
- [ ] `collectstatic` ejecutado
- [ ] WhiteNoise configurado
- [ ] Archivos sirviendo correctamente

### Logs
- [ ] Logging configurado
- [ ] Health check funcionando
- [ ] Error tracking activo

### Performance
- [ ] Gunicorn configurado
- [ ] Database pooling activo
- [ ] Rate limiting habilitado

---

## 1️⃣1️⃣ **Comandos Útiles**

### Crear Superusuario
```bash
python manage.py createsuperuser
```

### Ver Migraciones Pendientes
```bash
python manage.py showmigrations
```

### Ejecutar Migraciones
```bash
python manage.py migrate
```

### Recopilar Static Files
```bash
python manage.py collectstatic --noinput
```

### Ver Logs en Tiempo Real
```bash
# En Render Dashboard > Logs
# O vía CLI
render logs -f
```

### Reset Database (Cuidado!)
```bash
python manage.py flush
```

---

## 1️⃣2️⃣ **Troubleshooting**

### Error: "ALLOWED_HOSTS"
```
Solución: Agregar el dominio a ALLOWED_HOSTS en .env
ALLOWED_HOSTS=cerbero.onrender.com,localhost
```

### Error: "CSRF verification failed"
```
Solución: Agregar a CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS=https://cerbero.onrender.com
```

### Error: "Static files not found"
```bash
# Ejecutar
python manage.py collectstatic --noinput

# Verificar WhiteNoise en MIDDLEWARE
```

### Error: "Database connection failed"
```
Solución: Verificar DATABASE_URL en Render
Formato: postgresql://user:pass@host:5432/dbname
```

### Error: "502 Bad Gateway"
```
Solución:
1. Verificar logs en Render
2. Check Gunicorn configuration
3. Verificar puertos
```

---

## 1️⃣3️⃣ **Monitoreo Post-Despliegue**

### Métricas a Monitorear
- Response time (< 500ms ideal)
- Error rate (< 1%)
- Memory usage
- CPU usage
- Database connections

### Alertas Recomendadas
- Error 500 > 5 en 5 minutos
- Response time > 2 segundos
- Disk usage > 80%
- Database connections > 80%

---

## 1️⃣4️⃣ **Mejoras Futuras**

### CDN (CloudFlare)
- Cache de static files
- DDoS protection
- Mejor performance global

### Email Configuration
```python
# Para reset de passwords
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-password'
```

### Cache (Redis)
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}
```

### API Documentation
```bash
pip install drf-spectacular
```

### Testing
```bash
python manage.py test
```

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Render
2. Verifica variables de entorno
3. Comprueba migraciones
4. Testea health check endpoint

---

## ✅ Checklist Final

- [ ] Variables de entorno configuradas
- [ ] Base de datos PostgreSQL lista
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Static files recopilados
- [ ] HTTPS habilitado
- [ ] Logs funcionando
- [ ] Health check responde OK
- [ ] Rate limiting activo
- [ ] Backup configurado

**¡Tu proyecto está listo para producción! 🎉**
