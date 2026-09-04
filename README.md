<div align="center">
  <img src="https://raw.githubusercontent.com/wjfenix87-spec/Cerbero/main/cerbero/core/static/assets/logo_badass.png" alt="Cerbero Logo" width="150"/>
  <h1>CERBERO</h1>
  <p><strong>El guardián del contexto digital. Fricción cero entre tu código y las IAs.</strong></p>
  
  <a href="https://cerbero-w3f6.onrender.com/" target="_blank">
    <img src="https://img.shields.io/badge/Demo_en_Vivo-Cerbero-00f3ff?style=for-the-badge&logo=render" alt="Demo en Vivo" />
  </a>
</div>

---

## 🚀 ¿Qué es Cerbero?

Cerbero es una herramienta diseñada para desarrolladores que necesitan alimentar a las Inteligencias Artificiales (ChatGPT, Claude, Gemini, etc.) con el contexto completo de sus proyectos. 

En lugar de copiar y pegar cientos de archivos uno por uno, Cerbero procesa tu proyecto entero de forma **ultrarrápida y 100% local en tu navegador**, generando un único archivo unificado (`.txt` o `.md`) listo para ser analizado por la IA.

## ✨ Características Principales

- **Procesamiento 100% Local:** Tus archivos nunca abandonan tu computadora. Todo ocurre en la memoria RAM de tu navegador garantizando privacidad absoluta.
- **Filtro Inteligente:** Ignora automáticamente carpetas pesadas e irrelevantes como `node_modules`, `venv`, `.git`, binarios y dependencias.
- **Velocidad Extrema:** Procesa miles de archivos en cuestión de milisegundos gracias a la lectura paralela y extracción en memoria.
- **Formatos IA-Ready:** Extrae el código en formato crudo `.txt` o estructurado `.md` (Markdown), ideal para modelos de lenguaje.

## 🛠️ Cómo Funciona

Cerbero opera directamente desde la interfaz web (puedes probarlo ahora mismo en [cerbero-w3f6.onrender.com](https://cerbero-w3f6.onrender.com/)):
1. Arrastra la carpeta de tu proyecto a la **Zona de Transferencia**.
2. Selecciona el formato de salida deseado (`.txt` o `.md`).
3. Haz clic en "Generar y Descargar".
4. ¡Listo! Arrastra el archivo generado al chat de tu IA favorita.

## 💻 Instalación Local (Para Desarrolladores)

Cerbero está construido con un backend ligero en Django y un frontend reactivo en Vanilla JS.

### Requisitos
- Python 3.x
- Entorno virtual (recomendado)

### Pasos
1. Clona el repositorio:
   ```bash
   git clone https://github.com/wjfenix87-spec/Cerbero.git
   cd Cerbero
   ```
2. Activa tu entorno virtual e instala dependencias (si aplica).
3. Corre el servidor de desarrollo:
   ```bash
   cd cerbero
   python manage.py runserver
   ```
4. Abre `http://localhost:8000` en tu navegador.

## 🛡️ Privacidad

Cerbero fue construido bajo el principio fundamental de que **tu código es tuyo**. Al mover todo el procesamiento del lado del cliente utilizando las APIs de `FileReader` y `Blob`, es matemáticamente imposible que tu código fuente sea interceptado o subido a la nube.

---
*Construido para acelerar el desarrollo con Inteligencia Artificial.*
