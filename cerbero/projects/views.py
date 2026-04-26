from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from .models import Project, ProjectFile
from datetime import timedelta
import json
import zipfile
import tempfile
import os
import logging

logger = logging.getLogger('projects')

# File upload constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB per file
MAX_FILES_PER_UPLOAD = 100  # Maximum files per upload
ALLOWED_FILE_TYPES = [
    'text/x-python', 'text/javascript', 'application/javascript',
    'text/html', 'text/css', 'application/json', 'text/xml',
    'application/xml', 'text/x-java', 'text/x-c', 'text/x-c++',
    'text/x-php', 'text/x-ruby', 'text/x-go', 'text/x-rust',
    'text/x-typescript', 'text/x-script.python',
]


def project_view(request, slug):
    """Vista pública del proyecto - para que la IA vea el código"""
    project = get_object_or_404(Project, slug=slug)
    files = project.files.all()
    
    # Detectar framework y lenguaje
    framework, language = detect_framework_and_language(files)
    
    # Verificar expiración
    if project.is_expired():
        return render(request, 'core/expired.html', {'project': project})
    
    # Incrementar contador de vistas
    project.views += 1
    project.save()
    
    # Modo IA (texto plano para que la IA lea)
    if request.GET.get('mode') == 'ia' or request.GET.get('mode') == 'text':
        response = HttpResponse(content_type='text/plain; charset=utf-8')
        
        # Información del proyecto
        response.write("=" * 60 + "\n")
        response.write("INFORMACIÓN DEL PROYECTO\n")
        response.write("=" * 60 + "\n")
        response.write(f"Framework detectado: {framework}\n")
        response.write(f"Lenguaje: {language}\n")
        response.write(f"Archivos totales: {files.count()}\n")
        response.write("=" * 60 + "\n\n")
        
        for file in files:
            response.write(f"## {file.original_name}\n")
            response.write(f"Tamaño: {file.size} bytes\n")
            response.write("-" * 40 + "\n")
            
            try:
                with open(file.file.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 5000:
                        content = content[:5000] + "\n... [CONTENIDO TRUNCADO]"
                    response.write(content)
            except (UnicodeDecodeError, FileNotFoundError, OSError):
                response.write("[ARCHIVO BINARIO - No se puede mostrar en texto plano]")
            response.write("\n\n" + "=" * 60 + "\n\n")
        
        return response
    
    # Modo JSON
    if request.GET.get('mode') == 'json':
        return JsonResponse({
            'slug': project.slug,
            'title': project.title,
            'framework': framework,
            'language': language,
            'files': [{
                'name': f.original_name,
                'size': f.size,
                'url': f.file.url
            } for f in files]
        })
    
    # Modo humano (vista normal)
    return render(request, 'core/project.html', {
        'project': project,
        'files': files,
        'total_size': sum(f.size for f in files),
        'framework': framework,
        'language': language,
    })


def get_project_info(request, slug):
    """Obtener información del proyecto en JSON"""
    project = get_object_or_404(Project, slug=slug)
    files = project.files.all()
    
    return JsonResponse({
        'slug': project.slug,
        'title': project.title,
        'created_at': project.created_at.isoformat(),
        'expires_at': project.expires_at.isoformat() if project.expires_at else None,
        'views': project.views,
        'files': [{
            'name': f.original_name,
            'size': f.size,
            'type': f.file_type,
            'url': f.file.url
        } for f in files]
    })


@csrf_exempt
@require_http_methods(["POST"])
@throttle_classes([AnonRateThrottle])
def upload_file(request):
    """Endpoint para subir archivos"""
    try:
        slug = request.POST.get('slug')
        expiration_hours = request.POST.get('expiration')
        
        user = get_user_from_request(request)
        
        if slug:
            project = Project.objects.get(slug=slug)
        else:
            project = Project.objects.create(user=user)
            
            if expiration_hours:
                try:
                    hours = int(expiration_hours)
                    project.expires_at = timezone.now() + timedelta(hours=hours)
                    project.save()
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid expiration value: {expiration_hours} - {e}")
        
        files = request.FILES.getlist('files')
        
        # Validate file count
        if len(files) > MAX_FILES_PER_UPLOAD:
            return JsonResponse({
                'error': f'Demasiados archivos. Máximo permitido: {MAX_FILES_PER_UPLOAD}'
            }, status=400)
        
        uploaded_files = []
        
        for file in files:
            # Validate file size
            if file.size > MAX_FILE_SIZE:
                logger.warning(f"File too large: {file.name} ({file.size} bytes)")
                return JsonResponse({
                    'error': f'Archivo demasiado grande: {file.name}. Máximo: {MAX_FILE_SIZE // (1024*1024)}MB'
                }, status=400)
            
            project_file = ProjectFile.objects.create(
                project=project,
                file=file,
                original_name=file.name,
                size=file.size,
                file_type=file.content_type or 'application/octet-stream'
            )
            uploaded_files.append({
                'name': file.name,
                'size': file.size,
                'url': project_file.file.url
            })
        
        return JsonResponse({
            'success': True,
            'slug': project.slug,
            'url': f'/p/{project.slug}/',
            'full_url': request.build_absolute_uri(f'/p/{project.slug}/'),
            'files': uploaded_files,
            'count': len(uploaded_files),
            'user': user.username if user else None
        })
        
    except Project.DoesNotExist:
        logger.error(f"Project not found: {slug}")
        return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@throttle_classes([AnonRateThrottle])
def upload_folder(request):
    try:
        user = get_user_from_request(request)
        expiration_hours = request.POST.get('expiration')
        
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'error': 'No se subió ninguna carpeta'}, status=400)
        
        # ===== FILTRO DE ARCHIVOS BASURA =====
        IGNORE_FOLDERS = [
            'venv/', 'env/', '.venv/', '__pycache__/', '.git/',
            'node_modules/', '.idea/', '.vscode/', '.pytest_cache/',
            'build/', 'dist/', 'target/', '.gradle/', '.mvn/'
        ]
        
        IGNORE_EXTENSIONS = [
            '.pyc', '.pyo', '.so', '.dll', '.exe', '.log', 
            '.tmp', '.cache', '.DS_Store', 'Thumbs.db'
        ]
        
        IMPORTANT_EXTENSIONS = [
            '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml',
            '.md', '.txt', '.xml', '.sql', '.java', '.c', '.cpp', 
            '.h', '.php', '.rb', '.go', '.rs', '.ts', '.jsx', '.tsx'
        ]
        
        filtered_files = []
        ignored_count = 0
        
        for file in files:
            should_ignore = False
            
            # 1. Ignorar por carpeta
            for folder in IGNORE_FOLDERS:
                if folder in file.name.lower():
                    should_ignore = True
                    break
            
            # 2. Ignorar por extensión basura
            for ext in IGNORE_EXTENSIONS:
                if file.name.lower().endswith(ext):
                    should_ignore = True
                    break
            
            # 3. Si no es importante y no es extensión conocida, ignorar
            is_important = False
            for ext in IMPORTANT_EXTENSIONS:
                if file.name.lower().endswith(ext):
                    is_important = True
                    break
            
            # Archivos sin extensión importante y que no están en la lista blanca
            if not is_important and not should_ignore:
                # Conservar archivos de configuración comunes
                important_configs = ['dockerfile', 'makefile', 'readme', 'license', 'gitignore']
                if not any(cfg in file.name.lower() for cfg in important_configs):
                    should_ignore = True
            
            if should_ignore:
                ignored_count += 1
                continue
            
            filtered_files.append(file)
        
        print(f"📊 Archivos: {len(files)} totales → {len(filtered_files)} importantes → {ignored_count} ignorados")
        
        # ===== CREAR PROYECTO =====
        project = Project.objects.create(user=user)
        
        if expiration_hours:
            try:
                hours = int(expiration_hours)
                project.expires_at = timezone.now() + timedelta(hours=hours)
                project.save()
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid expiration value: {expiration_hours} - {e}")
        
        # ===== GUARDAR ARCHIVOS IMPORTANTES =====
        for file in filtered_files[:5000]:  # Límite de seguridad
            ProjectFile.objects.create(
                project=project,
                file=file,
                original_name=file.name,
                size=file.size,
                file_type=file.content_type or 'application/octet-stream'
            )
        
        return JsonResponse({
            'success': True,
            'slug': project.slug,
            'url': f'/p/{project.slug}/',
            'full_url': request.build_absolute_uri(f'/p/{project.slug}/'),
            'count': len(filtered_files),
            'ignored': ignored_count,
            'total': len(files)
        })
        
    except Exception as e:
        logger.error(f"Error uploading folder: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@throttle_classes([AnonRateThrottle])
def upload_zip(request):
    try:
        zip_file = request.FILES.get('zip_file')
        if not zip_file:
            return JsonResponse({'error': 'No se subió ningún archivo ZIP'}, status=400)
        
        user = get_user_from_request(request)
        expiration_hours = request.POST.get('expiration')
        
        project = Project.objects.create(user=user)
        
        if expiration_hours:
            try:
                hours = int(expiration_hours)
                project.expires_at = timezone.now() + timedelta(hours=hours)
                project.save()
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid expiration value: {expiration_hours} - {e}")
        
        # MISMAS LISTAS DE FILTRO
        IGNORE_FOLDERS = ['venv/', 'env/', '.venv/', '__pycache__/', '.git/', 'node_modules/', '.idea/', '.vscode/']
        IGNORE_EXTENSIONS = ['.pyc', '.pyo', '.so', '.dll', '.exe', '.log', '.tmp', '.cache']
        IMPORTANT_EXTENSIONS = ['.py', '.js', '.html', '.css', '.json', '.yaml', '.md', '.txt', '.xml', '.sql']
        
        import tempfile, zipfile, os
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, 'project.zip')
            with open(zip_path, 'wb') as f:
                for chunk in zip_file.chunks():
                    f.write(chunk)
            
            extracted_count = 0
            ignored_count = 0
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for file_info in zf.infolist():
                    if file_info.is_dir():
                        continue
                    
                    should_ignore = False
                    for folder in IGNORE_FOLDERS:
                        if folder in file_info.filename.lower():
                            should_ignore = True
                            break
                    
                    for ext in IGNORE_EXTENSIONS:
                        if file_info.filename.lower().endswith(ext):
                            should_ignore = True
                            break
                    
                    is_important = any(file_info.filename.lower().endswith(ext) for ext in IMPORTANT_EXTENSIONS)
                    if not is_important and not should_ignore:
                        should_ignore = True
                    
                    if should_ignore:
                        ignored_count += 1
                        continue
                    
                    content = zf.read(file_info)
                    from django.core.files.base import ContentFile
                    ProjectFile.objects.create(
                        project=project,
                        original_name=file_info.filename,
                        size=file_info.file_size,
                        file_type='application/octet-stream'
                    ).file.save(file_info.filename, ContentFile(content))
                    extracted_count += 1
        
        return JsonResponse({
            'success': True,
            'slug': project.slug,
            'url': f'/p/{project.slug}/',
            'full_url': request.build_absolute_uri(f'/p/{project.slug}/'),
            'count': extracted_count,
            'ignored': ignored_count
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_projects(request):
    """Lista de proyectos del usuario autenticado"""
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    
    return Response({
        'projects': [{
            'slug': p.slug,
            'title': p.title or p.slug,
            'created_at': p.created_at,
            'files_count': p.files.count(),
            'views': p.views,
            'url': f'/p/{p.slug}/'
        } for p in projects]
    })


@csrf_exempt
@require_http_methods(["PUT"])
def update_project(request, slug):
    """Actualizar título del proyecto"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    project = get_object_or_404(Project, slug=slug, user=request.user)
    
    try:
        data = json.loads(request.body)
        project.title = data.get('title', project.title)
        project.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_project(request, slug):
    """Eliminar proyecto y todos sus archivos"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    project = get_object_or_404(Project, slug=slug, user=request.user)
    
    for file in project.files.all():
        file.file.delete(save=False)
    
    project.delete()
    
    return JsonResponse({'success': True})


def get_user_from_request(request):
    """Obtener usuario del token JWT"""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        from rest_framework_simplejwt.tokens import AccessToken
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            token = auth_header.split(' ')[1]
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except Exception:
            pass
    return None

def download_for_ia(request, slug):
    """Descargar todo el código del proyecto en un archivo de texto para IAs"""
    project = get_object_or_404(Project, slug=slug)
    files = project.files.all()
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{slug}_proyecto.txt"'
    
    response.write(f"PROYECTO: {project.slug}\n")
    response.write(f"ARCHIVOS: {files.count()}\n")
    response.write("=" * 60 + "\n\n")
    
    for file in files:
        response.write(f"=== {file.original_name} ===\n")
        response.write(f"Tamaño: {file.size} bytes\n")
        response.write("-" * 40 + "\n")
        
        try:
            with open(file.file.path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Limitar a 5000 caracteres por archivo
                if len(content) > 5000:
                    content = content[:5000] + "\n... [CONTENIDO TRUNCADO]"
                response.write(content)
        except (UnicodeDecodeError, FileNotFoundError, OSError):
            response.write("[ARCHIVO BINARIO - No se puede mostrar en texto plano]")
        response.write("\n\n" + "=" * 60 + "\n\n")
    
    return response

def detect_framework_and_language(files):
    """Detecta el framework y lenguaje basado en los archivos del proyecto"""
    file_names = [f.original_name for f in files]
    file_names_lower = [f.lower() for f in file_names]
    
    # Django
    if 'manage.py' in file_names or 'settings.py' in file_names:
        return 'Django', 'Python'
    
    # Flask
    if 'app.py' in file_names or 'requirements.txt' in file_names:
        if any('flask' in f.lower() for f in file_names):
            return 'Flask', 'Python'
    
    # React
    if 'package.json' in file_names:
        if any('react' in f.lower() for f in file_names):
            return 'React', 'JavaScript/JSX'
        return 'Node.js', 'JavaScript'
    
    # Angular
    if 'angular.json' in file_names:
        return 'Angular', 'TypeScript'
    
    # Flutter
    if 'pubspec.yaml' in file_names:
        return 'Flutter', 'Dart'
    
    # Spring Boot
    if 'pom.xml' in file_names:
        return 'Spring Boot', 'Java'
    
    # HTML/CSS/JS puro
    if any(f.endswith('.html') for f in file_names):
        return 'HTML/CSS/JS', 'HTML/CSS/JavaScript'
    
    # Python puro
    if any(f.endswith('.py') for f in file_names):
        return 'Python', 'Python'
    
    return 'Desconocido', 'Desconocido'
