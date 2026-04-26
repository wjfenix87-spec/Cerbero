from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    """Vista principal - Devuelve el HTML"""
    return render(request, 'core/home.html')

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'ok',
        'message': 'Cerbero API funcionando 🐕',
        'version': '1.0.0'
    })

def upload_guide(request, framework):
    frameworks = {
        'django': {
            'name': 'Django',
            'icon': '🐍',
            'files': ['tu_app/', 'templates/', 'static/', 'manage.py', 'requirements.txt'],
            'extensions': ['.py', '.html', '.css', '.js'],
            'avoid': ['venv/', 'env/', '__pycache__/', '.git/', 'db.sqlite3'],
            'avoid_desc': 'Entorno virtual, archivos compilados, control de versiones, base de datos local'
        },
        'flutter': {
            'name': 'Flutter',
            'icon': '📱',
            'files': ['lib/', 'assets/', 'pubspec.yaml'],
            'extensions': ['.dart', '.yaml'],
            'avoid': ['build/', '.dart_tool/', '.idea/', '.vscode/'],
            'avoid_desc': 'Archivos compilados, cache de Dart, configuraciones del editor'
        },
        'react': {
            'name': 'React',
            'icon': '⚛️',
            'files': ['src/', 'public/', 'package.json'],
            'extensions': ['.js', '.jsx', '.css'],
            'avoid': ['node_modules/', 'build/', '.git/', 'dist/'],
            'avoid_desc': 'Dependencias, archivos compilados, control de versiones'
        },
        'angular': {
            'name': 'Angular',
            'icon': '🅰️',
            'files': ['src/app/', 'src/assets/', 'angular.json', 'package.json'],
            'extensions': ['.ts', '.html', '.css'],
            'avoid': ['node_modules/', 'dist/', '.git/', 'tmp/'],
            'avoid_desc': 'Dependencias, archivos compilados, control de versiones'
        },
        'vue': {
            'name': 'Vue.js',
            'icon': '💚',
            'files': ['src/', 'public/', 'package.json'],
            'extensions': ['.vue', '.js', '.css'],
            'avoid': ['node_modules/', 'dist/', '.git/'],
            'avoid_desc': 'Dependencias, archivos compilados, control de versiones'
        },
        'node': {
            'name': 'Node.js',
            'icon': '🟢',
            'files': ['src/', 'routes/', 'package.json', 'server.js'],
            'extensions': ['.js', '.json'],
            'avoid': ['node_modules/', '.git/', '.env', 'logs/'],
            'avoid_desc': 'Dependencias, control de versiones, variables secretas, logs'
        },
        'spring': {
            'name': 'Spring Boot',
            'icon': '🍃',
            'files': ['src/main/java/', 'src/main/resources/', 'pom.xml'],
            'extensions': ['.java', '.xml', '.properties'],
            'avoid': ['target/', '.git/', '.mvn/', '.gradle/'],
            'avoid_desc': 'Archivos compilados, control de versiones, cache de Maven/Gradle'
        },
        'laravel': {
            'name': 'Laravel',
            'icon': '🔴',
            'files': ['app/', 'routes/', 'resources/views/', 'composer.json'],
            'extensions': ['.php', '.blade.php'],
            'avoid': ['vendor/', 'node_modules/', '.git/', '.env', 'storage/logs/'],
            'avoid_desc': 'Dependencias, control de versiones, variables secretas, logs'
        },
        'html': {
            'name': 'HTML/CSS/JS',
            'icon': '📄',
            'files': ['index.html', 'css/', 'js/', 'assets/'],
            'extensions': ['.html', '.css', '.js'],
            'avoid': ['node_modules/', '.git/'],
            'avoid_desc': 'Dependencias, control de versiones'
        }
    }
    
    data = frameworks.get(framework, frameworks['html'])
    return render(request, 'core/upload_guide.html', {
        'framework': data,
        'framework_key': framework
    })