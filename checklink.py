import os  # Importa el módulo os para interactuar con el sistema de archivos
import re  # Importa el módulo re para trabajar con expresiones regulares
import requests  # Importa el módulo requests para realizar solicitudes HTTP

# Función para encontrar todos los archivos .md en un directorio dado
def find_md_files(directory):
    md_files = []  # Lista para almacenar las rutas de los archivos .md
    # Recorre el directorio y sus subdirectorios
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Si el archivo termina en .md, se añade a la lista
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files  # Devuelve la lista de archivos .md encontrados

# Función para extraer enlaces de un archivo .md
def extract_links(md_file):
    links = []  # Lista para almacenar los enlaces encontrados
    # Abre el archivo en modo lectura con codificación UTF-8
    with open(md_file, 'r', encoding='utf-8') as file:
        # Recorre cada línea del archivo
        for line_num, line in enumerate(file, 1):
            # Busca todos los enlaces en la línea usando una expresión regular
            for match in re.finditer(r'\[.*?\]\((.*?)\)', line):
                url = match.group(1)  # Extrae la URL del enlace
                col_num = match.start(1) + 1  # Calcula la columna donde empieza el enlace
                links.append((url, line_num, col_num))  # Añade la URL, línea y columna a la lista
    return links  # Devuelve la lista de enlaces encontrados

# Función para verificar si un enlace es válido
def check_link(url, base_path):
    # Si el enlace empieza con http:// o https://, se trata de un enlace web
    if url.startswith(('http://', 'https://')):
        try:
            # Realiza una solicitud HEAD para verificar el enlace
            response = requests.head(url, allow_redirects=True)
            return response.status_code == 200, None  # Devuelve True si el estado es 200 (OK)
        except requests.RequestException as e:
            return False, str(e)  # Devuelve False y el error si la solicitud falla
    else:
        # Si no es un enlace web, se trata de un enlace local
        local_path = os.path.join(base_path, url)  # Construye la ruta completa del archivo local
        return os.path.exists(local_path), "File not found" if not os.path.exists(local_path) else None  # Verifica si el archivo existe

# Función principal que coordina la verificación de enlaces
def main(directory):
    md_files = find_md_files(directory)  # Encuentra todos los archivos .md en el directorio
    broken_links = {}  # Diccionario para almacenar enlaces rotos
    for md_file in md_files:
        links = extract_links(md_file)  # Extrae los enlaces de cada archivo .md
        for url, line_num, col_num in links:
            is_valid, error = check_link(url, os.path.dirname(md_file))  # Verifica cada enlace
            if not is_valid:
                if md_file not in broken_links:
                    broken_links[md_file] = []
                broken_links[md_file].append((url, line_num, col_num, error))  # Añade el enlace roto al diccionario
    
    # Crea el directorio results si no existe
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Escribe los resultados en el archivo result.md
    with open('results/result.md', 'w', encoding='utf-8') as result_file:
        if broken_links:
            result_file.write("# Broken Links Report\n\n")
            for md_file, links in broken_links.items():
                result_file.write(f"## In file {md_file}:\n")
                for url, line_num, col_num, error in links:
                    result_file.write(f"- **Line {line_num}, Column {col_num}**: {url} - Error: {error}\n")
        else:
            result_file.write("No broken links found.\n")

# Ejecuta la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main('docs')
