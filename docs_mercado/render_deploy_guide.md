# Guía de Despliegue en Render.com

Esta guía contiene los pasos exactos para subir Cerbero v3.0 a internet de forma gratuita usando Render. Al no requerir bases de datos, el proceso es extremadamente sencillo.

## 1. Sube tu código a GitHub
Asegúrate de haber hecho `commit` y `push` de todos los últimos cambios de este proyecto a tu repositorio de GitHub.

## 2. Crear el Servicio Web en Render
1. Entra a [Render.com](https://render.com) e inicia sesión con GitHub.
2. Ve a tu panel (Dashboard), haz clic en **"New +"** y selecciona **"Web Service"**.
3. Selecciona tu repositorio de GitHub donde tienes el código de Cerbero.

## 3. Configurar el Servicio (MUY IMPORTANTE)
Llena el formulario con exactamente estos datos:

- **Name:** cerbero-app *(o el nombre que gustes)*
- **Environment:** Python 3
- **Region:** US (Ohio) *(o la que prefieras)*
- **Branch:** main *(o master)*

### Comandos de Ejecución
Aquí es donde le decimos a Render cómo construir e iniciar Cerbero.

- **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```

- **Start Command:**
  ```bash
  gunicorn config.wsgi:application
  ```

## 4. Variables de Entorno (Environment Variables)
Baja un poco más en la misma pantalla hasta llegar a la sección de **"Environment Variables"** y haz clic en "Add Environment Variable". Agrega estas dos:

1. **Key:** `DEBUG`
   **Value:** `False`

2. **Key:** `ALLOWED_HOSTS`
   **Value:** `*`
   *(Nota: Poner un asterisco permite que Django acepte peticiones desde el subdominio que Render te asigne automáticamente. En el futuro, si compras un dominio como cerbero.com, cambiarás el asterisco por cerbero.com).*

## 5. ¡A producción!
Haz clic en el botón verde **"Create Web Service"**.

Render abrirá una terminal y empezará a construir el proyecto. Este primer proceso puede tomar un par de minutos mientras instala Python y Gunicorn.
Cuando termine, el estado cambiará a **Live** y podrás acceder a tu página desde el enlace que aparece arriba a la izquierda (ej: `https://cerbero-app.onrender.com`).

¡Listo! Cerbero ya está en la nube devorando proyectos a la velocidad de la luz.
