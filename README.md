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

El proyecto se ha desarrollado con Python 3.14 (entorno verificado: Python 3.14.7). Las versiones registradas de sus dependencias están en `requirements.txt`. **La instalación desde cero todavía requiere validación** en un entorno limpio.

En PowerShell, dentro de la carpeta del proyecto (preferentemente con un entorno virtual):

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

## Compilación para Windows

### Herramientas y recursos

El entorno probado utiliza **Windows 11 x64**, **Python 3.14.7**, **PyInstaller 6.22.3** e **Inno Setup 6**. Las versiones de los paquetes Python, incluido `pi-heif==1.4.0`, están registradas en `requirements.txt`. Estas instrucciones describen el proceso utilizado, pero **todavía no se validó una compilación completa desde cero en un Windows limpio**.

El repositorio contiene `yolo11n.pt` y los modelos `models/realesrgan-x4plus.bin` y `models/realesrgan-x4plus.param`. El ejecutable `realesrgan-ncnn-vulkan.exe` **no se almacena en Git**; debe prepararse por separado.

### 1. Instalar dependencias

Desde PowerShell, ubicado en la carpeta del repositorio:

```powershell
py -m pip install -r requirements.txt
```

Se recomienda un entorno virtual dedicado para una compilación nueva. La disponibilidad de paquetes puede depender de la versión de Python y de Windows.

### 2. Preparar Real-ESRGAN

Si está disponible el archivo `preparar_realesrgan.ps1` en la copia del proyecto, ejecutarlo desde PowerShell:

```powershell
.\preparar_realesrgan.ps1
```

El script local utilizado en las pruebas descarga el ZIP oficial indicado en su código, verifica el SHA-256 del ZIP (`ABC02804E17982A3BF33675E4D471F91FA374E65B70167ABC09F31ACB412802D`) y extrae `realesrgan-ncnn-vulkan.exe` solo si su SHA-256 coincide con `07E49F7CBB4EDE01AE4DD4C399D3A7E5846E3D2085C3128EFF881E55CB7B1A0C`.

**Nota de reproducibilidad:** antes de considerar esta guía autosuficiente, comprobar que el script está efectivamente publicado en el repositorio y que la descarga funciona desde una copia nueva. No se deben descargar ejecutables de fuentes no verificadas.

### 3. Compilar con PyInstaller

Una vez presentes los recursos:

```powershell
py -m PyInstaller --noconfirm --clean SmartCrop.spec
```

La salida esperada es `dist\SmartCrop\SmartCrop.exe`, junto a `dist\SmartCrop\_internal\`. El archivo `SmartCrop.spec` incorpora modelos, dependencias y documentación legal. Las carpetas `build/`, `dist/` e `installer/` están excluidas de Git.

### 4. Revisar la dependencia Microsoft VCOMP140.DLL

En el equipo de desarrollo se comprobó el funcionamiento de una compilación con `dist\SmartCrop\_internal\VCOMP140.DLL`, versión **14.44.35211.0**, obtenida de la distribución x64 de Microsoft Visual Studio 2022 Build Tools. SHA-256 de la DLL probada:

```text
55ABA23CDCD6484FBB06F4155B8CA75ADFCE7A881F10AFD0C49457165E677164
```

Para inspeccionar la DLL de una compilación:

```powershell
(Get-Item ".\dist\SmartCrop\_internal\VCOMP140.DLL").VersionInfo.FileVersion
(Get-FileHash ".\dist\SmartCrop\_internal\VCOMP140.DLL" -Algorithm SHA256).Hash
Get-AuthenticodeSignature ".\dist\SmartCrop\_internal\VCOMP140.DLL"
```

**Importante:** el archivo `.spec` no garantiza por sí solo que se empaquete esa versión de la DLL. En las pruebas se sustituyó y verificó la DLL de la carpeta compilada **antes** de generar el instalador. La forma de obtenerla y redistribuirla debe respetar las condiciones de Microsoft; no se debe asumir que copiarla desde cualquier instalación de Windows es adecuado. Queda pendiente automatizar y validar este paso para una compilación reproducible.

### 5. Probar el ejecutable

```powershell
.\dist\SmartCrop\SmartCrop.exe
```

Comprobar importación, miniaturas, encuadre automático y manual, exportación JPG/PNG y mejora opcional con Real-ESRGAN. **La interfaz actual ofrece una sola opción de mejora por IA**; no hay controles separados para seleccionar 2× o 4×.

### 6. Crear el instalador con Inno Setup

Solo después de comprobar que existe `dist\SmartCrop\SmartCrop.exe` y de verificar las dependencias, ejecutar:

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" ".\SmartCropInstaller.iss"
```

El script de Inno Setup incorpora `dist\SmartCrop\*` y genera `installer\SmartCrop_Setup_1.0.0.exe`. La ubicación de Inno Setup puede variar según la instalación.

### 7. Validaciones pendientes antes de distribuir

- Repetir la compilación desde una copia nueva del repositorio y comprobar que se puede obtener Real-ESRGAN.
- Instalar y ejecutar el instalador en un Windows limpio, sin herramientas de desarrollo.
- Probar recortes, exportación y mejora por IA en hardware compatible con Vulkan.
- Verificar archivos legales incluidos, condiciones de redistribución de terceros y dependencias de Microsoft.
- Comprobar desinstalación y preparar una publicación de GitHub Releases solo cuando terminen estas validaciones.

La aplicación y el instalador **sí funcionaron en las pruebas realizadas en el equipo de desarrollo**. Esto no equivale a una validación en todos los equipos Windows.

## Licencias y distribución

El código de SmartCrop AI se publica bajo **AGPL-3.0**. Las bibliotecas y modelos de terceros mantienen sus propias licencias. Consultar `LICENSE`, `THIRD_PARTY_NOTICES.md`, `LICENSE-Real-ESRGAN.txt`, `LICENSE-LGPL-3.0.txt` y `QT_LGPL_COMPLIANCE.md`.

**Estado:** documentación de distribución en revisión. No se ha confirmado aún el cumplimiento de todas las obligaciones de terceros ni la compatibilidad de MSIX con LGPL-3.0; no presentar este documento como certificación legal.
