from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .utils import is_file_allowed, get_gitignore_spec
import logging
import os

logger = logging.getLogger('projects')

def get_markdown_lang(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    mapping = {
        '.py': 'python', '.js': 'javascript', '.jsx': 'jsx',
        '.ts': 'typescript', '.tsx': 'tsx', '.html': 'html',
        '.css': 'css', '.json': 'json', '.md': 'markdown',
        '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.cs': 'csharp',
        '.go': 'go', '.rs': 'rust', '.rb': 'ruby', '.php': 'php',
        '.sh': 'bash', '.yml': 'yaml', '.yaml': 'yaml', '.xml': 'xml',
        '.sql': 'sql', '.swift': 'swift', '.kt': 'kotlin',
        '.dart': 'dart', '.ex': 'elixir', '.exs': 'elixir',
        '.zig': 'zig', '.nim': 'nim', '.vue': 'vue', '.svelte': 'svelte'
    }
    return mapping.get(ext, ext.replace('.', ''))


@csrf_exempt
@require_http_methods(["POST"])
def upload_folder(request):
    try:
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'error': 'No se subió ninguna carpeta'}, status=400)
        
        paths = request.POST.getlist('paths')
        if not paths or len(paths) != len(files):
            paths = [f.name for f in files]
            
        # ===== BUSCAR .GITIGNORE =====
        gitignore_content = None
        for file, path in zip(files, paths):
            if path.endswith('.gitignore') or path.split('/')[-1] == '.gitignore':
                try:
                    gitignore_content = file.read()
                    file.seek(0)
                    break
                except Exception:
                    pass
        
        spec = get_gitignore_spec(gitignore_content)
        
        # ===== FILTRO DE ARCHIVOS BASURA =====
        filtered_files = []
        ignored_count = 0
        
        for file, path in zip(files, paths):
            if is_file_allowed(path, spec):
                filtered_files.append((file, path))
            else:
                ignored_count += 1
        
        if not filtered_files:
            return JsonResponse({'error': 'El proyecto está vacío, dañado o no contiene código fuente válido.'}, status=400)
        
        # ===== GENERAR ARCHIVO TXT =====
        response_lines = []
        response_lines.append("=" * 60)
        response_lines.append("CONTEXTO DE PROYECTO PARA INTELIGENCIA ARTIFICIAL (Vía Cerbero)")
        response_lines.append("=" * 60)
        response_lines.append("¡Hola! Te presento el código fuente completo de este proyecto.")
        response_lines.append("A continuación encontrarás la estructura y el contenido de todos")
        response_lines.append("los archivos relevantes. Por favor, lee y analiza todo este")
        response_lines.append("contexto antes de responder a mis consultas o sugerir cambios.")
        response_lines.append("")
        response_lines.append(f"Archivos de código procesados: {len(filtered_files)}")
        response_lines.append(f"Archivos irrelevantes ignorados: {ignored_count}")
        response_lines.append("=" * 60 + "\n")
        
        for file, path in filtered_files:
            response_lines.append(f"## {path}")
            response_lines.append("-" * 40)
            
            try:
                content = file.read().decode('utf-8')
                if len(content) > 25000:
                    content = content[:25000] + "\n... [CONTENIDO TRUNCADO]"
                
                lang = get_markdown_lang(path)
                response_lines.append(f"```{lang}")
                response_lines.append(content)
                response_lines.append("```")
                
            except UnicodeDecodeError:
                response_lines.append("[ARCHIVO BINARIO - Ignorado]")
            except Exception as e:
                response_lines.append(f"[ERROR LEYENDO ARCHIVO: {e}]")
                
            response_lines.append("\n" + "=" * 60 + "\n")
            
        txt_content = "\n".join(response_lines)
        
        response = HttpResponse(txt_content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="cerbero_proyecto.txt"'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response
        
    except Exception as e:
        logger.error(f"Error processing folder: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
