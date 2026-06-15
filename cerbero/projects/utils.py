from django.utils import timezone
from datetime import timedelta
import logging
import pathspec

logger = logging.getLogger('projects')

DEFAULT_GITIGNORE = """
# Entornos virtuales y dependencias
venv/
env/
.venv/
node_modules/
vendor/
.bundle/

# Archivos compilados y cache
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.coverage
build/
dist/
target/
.gradle/
.mvn/
out/
bin/
obj/

# IDEs y configuración local
.idea/
.vscode/
.vs/
*.swp
*.swo
.DS_Store
Thumbs.db
.env
.env.local

# Logs y temporales
*.log
*.tmp
*.cache
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""

def get_gitignore_spec(custom_content=None):
    """
    Crea un objeto pathspec combinando las reglas por defecto y las del usuario.
    """
    lines = DEFAULT_GITIGNORE.splitlines()
    if custom_content:
        # Decodificar si viene como bytes
        if isinstance(custom_content, bytes):
            try:
                custom_content = custom_content.decode('utf-8')
            except UnicodeDecodeError:
                pass
        
        if isinstance(custom_content, str):
            lines.extend(custom_content.splitlines())
            
    return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, lines)

def is_file_allowed(filename, spec=None):
    """
    Verifica si un archivo debe ser permitido.
    Si el archivo hace "match" con el spec del gitignore, es ignorado (False).
    """
    if not spec:
        spec = get_gitignore_spec()
        
    # Si hace match con una regla de ignorar, NO es permitido
    if spec.match_file(filename):
        return False
        
    return True

