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

El proyecto se ha desarrollado con Python 3.14. **El 06/11/2026 se validó la instalación de dependencias en un entorno virtual nuevo con Python 3.14.7**, seguida de una compilación PyInstaller y pruebas funcionales satisfactorias en el equipo de desarrollo. Las versiones registradas de las dependencias están en `requirements.txt`. **No se ha probado todavía todo el procedimiento en una instalación limpia de Windows.**

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

El entorno probado utiliza **Windows 11 x64**, **Python 3.14.7**, **PyInstaller 6.22.3** e **Inno Setup 6** para el instalador tradicional. Las versiones de los paquetes Python, incluidos `pi-heif==1.4.0` y `lap==0.5.14`, están registradas en `requirements.txt`. **Se validó una reconstrucción en un entorno virtual nuevo en el equipo de desarrollo; sigue pendiente probar el procedimiento completo en un Windows limpio sin herramientas de desarrollo.**

El repositorio contiene `yolo11n.pt` y los modelos `models/realesrgan-x4plus.bin` y `models/realesrgan-x4plus.param`. El ejecutable `realesrgan-ncnn-vulkan.exe` **no se almacena en Git**; debe prepararse por separado.

### 1. Instalar dependencias

Desde PowerShell, ubicado en la carpeta del repositorio:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

El entorno virtual nuevo con Python 3.14.7 superó `pip check` el 06/11/2026. La disponibilidad de paquetes puede depender de la versión de Python y de Windows.

### 2. Preparar Real-ESRGAN

El repositorio incluye `preparar_realesrgan.ps1`. Revisar el script y sus orígenes antes de ejecutarlo:

```powershell
.\preparar_realesrgan.ps1
```

El script descarga el ZIP oficial indicado en su código, verifica el SHA-256 del ZIP (`ABC02804E17982A3BF33675E4D471F91FA374E65B70167ABC09F31ACB412802D`) y extrae `realesrgan-ncnn-vulkan.exe` solo si su SHA-256 coincide con `07E49F7CBB4EDE01AE4DD4C399D3A7E5846E3D2085C3128EFF881E55CB7B1A0C`.

**Nota de reproducibilidad:** el script está publicado en el repositorio, pero todavía debe verificarse su ejecución completa desde una copia nueva y la descarga efectiva del ZIP con el hash esperado. No se deben descargar ejecutables de fuentes no verificadas.

### 3. Compilar con PyInstaller

Una vez presentes los recursos, para la distribución tradicional:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean SmartCrop.spec
```

La salida esperada es `dist\SmartCrop\SmartCrop.exe`, junto a `dist\SmartCrop\_internal\`. El archivo `SmartCrop.spec` incorpora modelos, dependencias y documentación legal. Las carpetas `build/`, `dist/` e `installer/` están excluidas de Git.

**Compilación para Microsoft Store:** utiliza `main_store.py` y `SmartCrop_Store.spec`, no el archivo `.spec` tradicional. El procedimiento de reconstrucción y empaquetado MSIX está documentado en `BUILD_STORE_FROM_SOURCE.md`. Se validó una compilación Store en un entorno virtual nuevo y la generación de un MSIX de prueba sin firma; **no se acreditó identidad binaria del MSIX certificado ni se instaló el paquete de prueba**.

### 4. Revisar la dependencia Microsoft VCOMP140.DLL

En el equipo de desarrollo se comprobó el funcionamiento de una compilación con `dist\SmartCrop\_internal\VCOMP140.DLL`, versión **14.44.35211.0**, obtenida de la distribución x64 de Microsoft Visual Studio 2022 Build Tools. SHA-256 de la DLL probada:

```text
55ABA23CDCD6484FBB06F4155B8CA75ADFCE7A881F10AFD0C49457165E677164
```

Para inspeccionar la DLL de una compilación tradicional:

```powershell
(Get-Item ".\dist\SmartCrop\_internal\VCOMP140.DLL").VersionInfo.FileVersion
(Get-FileHash ".\dist\SmartCrop\_internal\VCOMP140.DLL" -Algorithm SHA256).Hash
Get-AuthenticodeSignature ".\dist\SmartCrop\_internal\VCOMP140.DLL"
```

**Importante:** el archivo `.spec` no garantiza por sí solo que se empaquete esa versión de la DLL. En las pruebas se sustituyó y verificó la DLL de la carpeta compilada **antes** de generar el instalador. La forma de obtenerla y redistribuirla debe respetar las condiciones de Microsoft; no se debe asumir que copiarla desde cualquier instalación de Windows es adecuado. Queda pendiente automatizar y validar este paso para una compilación reproducible. La compilación Store contiene una versión y ubicación distintas; consultar `BUILD_STORE_FROM_SOURCE.md`.

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

- Repetir el procedimiento completo desde una copia nueva del repositorio, incluida la descarga verificada de Real-ESRGAN.
- Instalar y ejecutar el instalador en un Windows limpio, sin herramientas de desarrollo.
- Probar recortes, exportación y mejora por IA en hardware compatible con Vulkan.
- Verificar archivos legales incluidos, condiciones de redistribución de terceros y dependencias de Microsoft.
- Comprobar desinstalación y revisar la publicación o actualización de GitHub Releases cuando terminen las validaciones.
- Para Microsoft Store, resolver por separado las obligaciones LGPL de la instalación MSIX y revisar las obligaciones AGPL de Ultralytics y demás licencias aplicables antes de publicar.

La aplicación y el instalador **sí funcionaron en las pruebas realizadas en el equipo de desarrollo**. Esto no equivale a una validación en todos los equipos Windows.

## Licencias y distribución

El código de SmartCrop AI se publica bajo **AGPL-3.0**. Las bibliotecas y modelos de terceros mantienen sus propias licencias. Consultar `LICENSE`, `THIRD_PARTY_NOTICES.md`, `LICENSE-Real-ESRGAN.txt`, `LICENSE-LGPL-3.0.txt`, `QT_LGPL_COMPLIANCE.md`, `QT_SOURCE_CODE.md` y `QT_REBUILD_AND_REPLACEMENT.md`.

**Estado:** documentación de distribución en revisión. No se ha confirmado aún el cumplimiento de todas las obligaciones de terceros ni la compatibilidad de MSIX con LGPL-3.0; no presentar este documento como certificación legal. La certificación técnica del MSIX 1.0.1.0 por Microsoft Store no resuelve esas cuestiones.
