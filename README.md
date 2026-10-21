# SmartCrop AI

Aplicación de escritorio para Windows (x64) que permite recortar imágenes en lotes mediante detección de personas y objetos con YOLO, ajustar el encuadre y exportar fotografías. La mejora opcional de resolución usa Real-ESRGAN NCNN Vulkan.

## Estado del proyecto

Código fuente de la versión 1.0.0. Este repositorio **todavía requiere revisión de licencias y pruebas de compilación** antes de anunciarse como distribución definitiva.

## Requisitos

- Windows x64, Python y dependencias de `requirements.txt`. La versión usada durante el desarrollo fue Python 3.14.
- Modelo `yolo11n.pt` junto a `main.py` (descarga y licencia: consultar Ultralytics).
- Para mejora opcional: `realesrgan-ncnn-vulkan.exe` y carpeta `models/` junto a `main.py`, con GPU/controladores Vulkan compatibles.

## Instalación para desarrollo

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

El proyecto no incluye binarios ni pesos de modelos de terceros. Consultar `THIRD_PARTY_NOTICES.md`.

## Compilación

Una vez descargados los recursos externos y comprobadas sus licencias:

```powershell
pyinstaller SmartCrop.spec
```

El script `SmartCropInstaller.iss` crea un instalador Inno Setup a partir de `dist/SmartCrop/`.

## Privacidad

El código suministrado no implementa telemetría ni carga de fotografías a servidores. La ejecución de librerías de terceros y sus posibles comportamientos de red deben verificarse por separado.

## Licencia


## Licencia

El código original de SmartCrop AI se distribuye bajo
GNU Affero General Public License v3.0 (AGPL-3.0-only).

Consultá el archivo [LICENSE](LICENSE) para conocer
los términos completos.

SmartCrop AI utiliza componentes de terceros, incluidos
Ultralytics YOLO, PySide6, PyTorch y Real-ESRGAN NCNN Vulkan,
que conservan sus respectivas licencias.

Consultá [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
para obtener más información sobre estos componentes.

