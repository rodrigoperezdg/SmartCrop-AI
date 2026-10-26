# SmartCrop AI

Aplicación de escritorio para **Windows** que prepara y recorta imágenes por lotes, con asistencia de IA y ajuste manual del encuadre.

## Funciones comprobadas en `main.py`

- Selección de varias fotografías y visualización de miniaturas con el recorte previsto.
- Encuadre automático asistido por **YOLO11n** (personas y objetos) y detección de rostros con OpenCV.
- Ajuste manual mediante arrastre, zoom y editor ampliado; opción de restaurar el encuadre automático.
- Formatos de salida: **1920 × 880**, **1920 × 1080**, **1080 × 1350** y **1080 × 1920**.
- Exportación **JPG** o **PNG**, con prefijos y sufijos configurables.
- Indicador de resolución de la imagen de origen.
- Mejora opcional con **Real-ESRGAN NCNN Vulkan**, modelo `realesrgan-x4plus` (4× nativo y redimensionamiento final LANCZOS).
- Controles para vigilar una carpeta, detener la vigilancia y limpiar la selección.
- Registro opcional del formato **AVIF** mediante `pillow-avif-plugin`.

## Código fuente

https://github.com/rodrigoperezdg/SmartCrop-AI

## Desarrollo en Windows

El proyecto se ha desarrollado con Python 3.14. Las versiones registradas de sus dependencias están en `requirements.txt`. **La instalación desde cero todavía requiere validación** en un entorno limpio.

En PowerShell, dentro de la carpeta del proyecto:

```powershell
py -m pip install -r requirements.txt
py main.py
```

El programa también necesita los recursos locales indicados a continuación; `pip` no los descarga automáticamente:

```text
SmartCrop/
  main.py
  yolo11n.pt
  realesrgan-ncnn-vulkan.exe
  models/
    realesrgan-x4plus.bin
    realesrgan-x4plus.param
```

El archivo `README_windows.md` incluido con Real-ESRGAN es documentación del proyecto externo, no el README principal de SmartCrop.

## Compilación

Se utiliza `SmartCrop.spec` con PyInstaller y un instalador opcional de Inno Setup (`SmartCropInstaller.iss`). El archivo `.spec` incluye explícitamente `pi_heif`; falta confirmar su versión en el entorno y reflejarla en `requirements.txt`.

No se recomienda publicar un nuevo instalador sin verificar que abre, genera miniaturas y exporta con y sin Real-ESRGAN.

## Licencias y distribución

El código de SmartCrop AI se publica bajo **AGPL-3.0**. Las bibliotecas y modelos de terceros mantienen sus propias licencias. Consultar `LICENSE`, `THIRD_PARTY_NOTICES.md`, `LICENSE-Real-ESRGAN.txt`, `LICENSE-LGPL-3.0.txt` y `QT_LGPL_COMPLIANCE.md`.

**Estado:** documentación de distribución en revisión. No se ha confirmado aún el cumplimiento de todas las obligaciones de terceros ni la compatibilidad de MSIX con LGPL-3.0; no presentar este documento como certificación legal.
