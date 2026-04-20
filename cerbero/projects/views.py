from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project, ProjectFile
from datetime import datetime, timedelta
import json
import zipfile
import tempfile
import os


def project_view(request, slug):
    """Vista pública del proyecto - para que la IA vea el código"""
    project = get_object_or_404(Project, slug=slug)
    files = project.files.all()
    
    # Verificar expiración
    if project.is_expired():
        return render(request, 'core/expired.html', {'project': project})
    
    # Incrementar contador de vistas
    project.views += 1
    project.save()
    
    # Modo IA (texto plano para que la IA lea)
    if request.GET.get('mode') == 'ia' or request.GET.get('mode') == 'text':
        response = HttpResponse(content_type='text/plain; charset=utf-8')
        response.write(f"# PROYECTO: {project.title or project.slug}\n")
        response.write(f"# ARCHIVOS: {files.count()}\n")
        response.write(f"# VISTAS: {project.views}\n")
        response.write("=" * 60 + "\n\n")
        
        for file in files:
            response.write(f"## {file.original_name}\n")
            response.write(f"Tamaño: {file.size} bytes\n")
            response.write("-" * 40 + "\n")
            
            try:
                # Intentar leer el archivo como texto
                with open(file.file.path, 'r', encoding='utf-8') as f:
                    content = f.read()
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
            'files': [{
                'name': f.original_name,
                'size': f.size,
                'url': f.file.url
            } for f in files]
        })
    
    # Modo humano
    return render(request, 'core/project.html', {
        'project': project,
        'files': files,
        'total_size': sum(f.size for f in files)
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
                    project.expires_at = datetime.now() + timedelta(hours=hours)
                    project.save()
                except:
                    pass
        
        files = request.FILES.getlist('files')
        uploaded_files = []
        
        for file in files:
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
        return JsonResponse({'error': 'Proyecto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def upload_folder(request):
    """Subir carpeta completa con estructura"""
    try:
        user = get_user_from_request(request)
        expiration_hours = request.POST.get('expiration')
        
        project = Project.objects.create(user=user)
        
        if expiration_hours:
            try:
                hours = int(expiration_hours)
                project.expires_at = datetime.now() + timedelta(hours=hours)
                project.save()
            except:
                pass
        
        files = request.FILES.getlist('files')
        paths = request.POST.getlist('paths')
        
        uploaded_files = []
        for i, file in enumerate(files):
            file_path = paths[i] if i < len(paths) else file.name
            
            project_file = ProjectFile.objects.create(
                project=project,
                file=file,
                original_name=file_path,
                size=file.size,
                file_type=file.content_type or 'application/octet-stream'
            )
            uploaded_files.append({'name': file_path, 'size': file.size})
        
        return JsonResponse({
            'success': True,
            'slug': project.slug,
            'url': f'/p/{project.slug}/',
            'full_url': request.build_absolute_uri(f'/p/{project.slug}/'),
            'count': len(uploaded_files),
            'files': uploaded_files
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def upload_zip(request):
    """Subir y descomprimir archivo ZIP"""
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
                project.expires_at = datetime.now() + timedelta(hours=hours)
                project.save()
            except:
                pass
        
        # Descomprimir en directorio temporal
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, 'project.zip')
            
            with open(zip_path, 'wb') as f:
                for chunk in zip_file.chunks():
                    f.write(chunk)
            
            extracted_count = 0
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for file_info in zf.infolist():
                    if file_info.is_dir():
                        continue
                    
                    content = zf.read(file_info)
                    from django.core.files.base import ContentFile
                    
                    project_file = ProjectFile(
                        project=project,
                        original_name=file_info.filename,
                        size=file_info.file_size,
                        file_type='application/octet-stream'
                    )
                    project_file.file.save(file_info.filename, ContentFile(content))
                    extracted_count += 1
        
        return JsonResponse({
            'success': True,
            'slug': project.slug,
            'url': f'/p/{project.slug}/',
            'full_url': request.build_absolute_uri(f'/p/{project.slug}/'),
            'count': extracted_count
        })
        
    except zipfile.BadZipFile:
        return JsonResponse({'error': 'El archivo no es un ZIP válido'}, status=400)
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