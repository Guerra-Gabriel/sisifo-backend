import os
import re

# Función para obtener todas las dependencias importadas en un archivo Python
def get_imports_from_file(file_path):
    imports = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
        for line in content:
            # Buscamos las líneas que contienen importaciones
            match = re.match(r'^\s*(import|from)\s+(\S+)', line)
            if match:
                module = match.group(2)
                imports.append(module)
    return imports

# Función para recorrer todos los archivos .py en directorios específicos
def get_all_imports_in_directory(directory, allowed_dirs):
    all_imports = set()
    # Recorremos solo los directorios especificados
    for subdir, _, files in os.walk(directory):
        # Excluir directorios que no son relevantes
        if any(excluded_dir in subdir for excluded_dir in allowed_dirs['exclude']):
            continue
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                imports = get_imports_from_file(file_path)
                all_imports.update(imports)
    return all_imports

# Filtra las dependencias estándar de Python y las importaciones internas del proyecto
def filter_standard_libraries_and_internal(all_imports, project_name, exclude_modules):
    # Librerías estándar de Python que no necesitan ser incluidas en requirements.txt
    standard_libraries = {
        'os', 'sys', 're', 'json', 'datetime', 'math', 'time', 'sqlite3', 'pdb', 'http', 'io', 'unittest', 'argparse',
        'shutil', 'subprocess', 'configparser', 'socket', 'hashlib', 'string', 'random', 'itertools', 'functools', 'collections',
        'email', 'socket', 'base64', 'xml', 'platform', 'struct', 'abc', 'glob', 'pickle', 'csv', 'urllib', 'http', 'bisect', 'dataclasses',
        'getpass', 'typing'
    }

    # Filtramos solo las librerías de terceros que no sean internas del proyecto ni módulos excluidos
    external_libraries = [
        lib for lib in all_imports 
        if lib not in standard_libraries 
        and not lib.startswith(project_name)  # Excluye cualquier importación que comience con el nombre del proyecto
        and not any(lib.startswith(exclude) for exclude in exclude_modules)  # Excluye módulos específicos como 'app'
        and '.' not in lib  # Excluye submódulos como 'werkzeug.security'
    ]
    return external_libraries

# Guardar las librerías en un archivo requirements.txt (sin versiones)
def save_requirements(libraries):
    with open('requirements.txt', 'w') as f:
        for library in libraries:
            f.write(f'{library}\n')

# Directorio donde está tu proyecto
project_directory = '/opt/projects/sisifo-backend'  # Actualiza con la ruta de tu proyecto
project_name = 'sisifo'  # Nombre del proyecto para filtrar las importaciones internas

# Módulos que deseas excluir explícitamente (como 'app' y otros)
exclude_modules = ['app', 'flask.json', 'werkzeug.security', 'flask_sqlalchemy']

# Directorios permitidos y excluidos
allowed_dirs = {
    'include': ['src', 'app', 'lib'],  # Asegúrate de que tu código está dentro de estos directorios
    'exclude': ['dist', 'build', 'venv', 'pip', 'test', '__pycache__', 'node_modules']  # Excluir directorios no relevantes
}

# Obtener todas las importaciones en el proyecto
all_imports = get_all_imports_in_directory(project_directory, allowed_dirs)

# Filtrar las importaciones de librerías externas
external_libraries = filter_standard_libraries_and_internal(all_imports, project_name, exclude_modules)

# Guardar en requirements.txt
save_requirements(external_libraries)

print("requirements.txt ha sido generado correctamente (sin versiones).")
