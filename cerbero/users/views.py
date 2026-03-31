from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from projects.models import Project
import json


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Registro de nuevos usuarios"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Usuario y contraseña requeridos'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """Login de usuarios"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
        
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Obtener información del usuario autenticado"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'bio': user.bio,
        'avatar': user.avatar,
        'created_at': user.created_at
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout (invalida refresh token)"""
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'success': True})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Obtener o actualizar perfil del usuario"""
    user = request.user
    
    if request.method == 'GET':
        projects_count = Project.objects.filter(user=user).count()
        total_views = sum(p.views for p in Project.objects.filter(user=user))
        total_files = sum(p.files.count() for p in Project.objects.filter(user=user))
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'avatar': user.avatar,
            'created_at': user.created_at,
            'stats': {
                'projects': projects_count,
                'views': total_views,
                'files': total_files
            }
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user.bio = data.get('bio', user.bio)
            user.avatar = data.get('avatar', user.avatar)
            user.save()
            
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'bio': user.bio,
                    'avatar': user.avatar
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)


def profile_page(request):
    """Vista HTML para la página de perfil"""
    return render(request, 'core/profile.html')