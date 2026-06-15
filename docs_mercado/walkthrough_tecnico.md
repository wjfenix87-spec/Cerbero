# Cerbero v3.0 - Walkthrough Técnico

> [!NOTE]
> Este documento describe la arquitectura y las decisiones técnicas detrás de la refactorización de Cerbero a su versión 3.0 (Fricción Cero).

## 1. Filosofía de Arquitectura
Cerbero pasó de ser una aplicación monolítica con bases de datos y persistencia a ser una **herramienta utilitaria de procesamiento en memoria**. 
Se eliminó la base de datos, el sistema de usuarios y la generación de enlaces públicos para priorizar:
- Privacidad absoluta (código nunca se guarda).
- Velocidad máxima (procesamiento en memoria).
- Fricción cero (sin registros ni logins).

## 2. El Frontend (Modo Dios)
El frontend fue rediseñado usando Vanilla JS y CSS moderno para evitar dependencias pesadas.
- **Drag & Drop Inteligente:** Utiliza el atributo `webkitdirectory` para permitir arrastrar carpetas enteras.
- **Filtro de Basura del lado del Cliente:** Antes de enviar datos, el frontend descarta archivos pesados como `.mp4`, `.exe` o carpetas `node_modules` para ahorrar ancho de banda.
- **Animaciones CSS "Modo Dios":** Se usan keyframes para simular un agujero negro digital y la API de Web Audio para sintetizar sonidos Sci-Fi nativos (sin archivos mp3).

## 3. El Backend (Motor Django)
- **Ruta Única:** `/api/upload-folder/` es el único endpoint que hace el trabajo.
- **CSRF Exempt:** Al ser una herramienta pública sin estado, se desactivó la validación CSRF para esta ruta.
- **Límites Desactivados:** Se configuró `DATA_UPLOAD_MAX_NUMBER_FIELDS = None` en `settings.py` para permitir la subida masiva de parámetros cuando los proyectos superan los 1000 archivos.
- **Generación Dinámica de Markdown:** El backend lee las extensiones de los archivos y los envuelve dinámicamente en bloques de sintaxis Markdown (ej. ` ```rust `), optimizando el `.txt` resultante para que las inteligencias artificiales (ChatGPT, Claude) lo lean con resaltado de sintaxis.

## 4. Seguridad
Toda la extracción de código ocurre bajo demanda. Al usar `file.read().decode('utf-8')` y manejar `UnicodeDecodeError`, evitamos que binarios maliciosos rompan el generador o ejecuten código remoto.
