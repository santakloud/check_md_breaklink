# check_md_breaklink
Este proyecto comprueba en la carpeta docs todos los directorio y subdirectorio y realiza un check de los diferentes links para ver si estan o no rotos

Este script en Python recorre un directorio llamado `docs`, busca archivos `.md`, extrae los enlaces y verifica si están rotos. Los resultados se guardan en un archivo `result.md` en el directorio `results`.

## Requisitos

- Python 3.x
- Módulo `requests`

Puedes instalar el módulo `requests` usando pip:

```sh
pip install requests
```
### Uso

Coloca el script en el directorio raíz de tu proyecto.
Asegúrate de que el directorio `docs` contenga los archivos `.md` que deseas verificar.
Ejecuta el script:

```sh
python script_name.py
```

### Resultados
El script generará un archivo result.md en el directorio results con el siguiente formato:

- Broken Links Report

- In file docs/example.md:
- **Line 10, Column 15**: https://example.com - Error: 404 Client Error: Not Found for url: https://example.com
- **Line 20, Column 5**: imgs/image1.png - Error: File not found

### Funciones Principales

find_md_files(directory): Recorre el directorio y encuentra todos los archivos .md.
extract_links(md_file): Extrae todos los enlaces de un archivo .md usando una expresión regular.
check_link(url, base_path): Verifica si un enlace no está roto haciendo una solicitud HTTP HEAD para enlaces web o comprobando la existencia de archivos locales.
main(directory): Junta todo, busca archivos .md, extrae los enlaces y verifica si están rotos, luego imprime los resultados en result.md.

### Estructura del Código

Importaciones: Importa los módulos necesarios (os, re, requests).
find_md_files(directory): Encuentra todos los archivos .md en el directorio especificado.
extract_links(md_file): Extrae los enlaces de cada archivo .md.
check_link(url, base_path): Verifica si los enlaces son válidos.
main(directory): Coordina la verificación de enlaces y genera el informe.

#### Contribuciones
Si deseas contribuir a este proyecto, por favor, abre un issue o envía un pull request.
