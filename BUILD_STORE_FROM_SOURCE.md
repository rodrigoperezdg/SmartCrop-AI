# SmartCrop AI — Compilación desde el código fuente (Windows / Microsoft Store)

**Estado:** procedimiento documentado, **pendiente de validación integral en un entorno limpio**. No se garantiza que el resultado sea idéntico, byte por byte, al MSIX certificado `1.0.1.0`. Este documento **no acredita cumplimiento de LGPL, AGPL ni de otras licencias**.

## 1. Alcance y entorno conocido

- Repositorio: <https://github.com/rodrigoperezdg/SmartCrop-AI>.
- Windows x64; Python **3.14.0**; PyInstaller **6.22.3**.
- Compilación de la aplicación Store: `main_store.py` y `SmartCrop_Store.spec`.
- Paquete Store de referencia: `SmartCropAI_1.0.1.0_Store.msix`, identidad `eskimal.SmartCropAI`, arquitectura `x64`, mínimo Windows `10.0.19041.0`.
- Windows SDK observado: `10.0.26100.0`, con `makeappx.exe` x64.
- Visual Studio Build Tools 2022 utilizado en pruebas de Qt.

Las versiones fijadas de bibliotecas Python están en `requirements.txt`: PySide6 6.11.2, ultralytics 8.4.157, opencv-python 4.12.0.88, numpy 2.2.6, Pillow 12.3.0, pillow-avif-plugin 1.6.0, torch 2.14.0, torchvision 0.29.0 y pi-heif 1.4.0. **No se ha comprobado todavía la instalación de este conjunto desde cero**. La presencia de `pi-heif` en `requirements.txt` no implica que esté instalado en cualquier intérprete Python utilizado.

## 2. Obtener el código y preparar dependencias

En PowerShell, desde una carpeta de trabajo:

```powershell
 git clone https://github.com/rodrigoperezdg/SmartCrop-AI.git
 cd SmartCrop-AI
 py -3.14 -m venv .venv
 .\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

El archivo `.spec` requiere además recursos que **no se instalan con pip**:

- `yolo11n.pt` en la raíz del repositorio.
- `models/realesrgan-x4plus.bin` y `models/realesrgan-x4plus.param`.
- `realesrgan-ncnn-vulkan.exe` en la raíz, preparado mediante `preparar_realesrgan.ps1` y verificación de sus hashes.
- `Assets/SmartCrop_Master.png`, `Assets/SmartCrop.ico` y los avisos/licencias incluidos en `SmartCrop_Store.spec`.

Ejecutar `preparar_realesrgan.ps1` **solo después de revisar el script y sus orígenes**. Si alguno de estos archivos no está disponible, la compilación debe detenerse: no se deben inventar pesos, modelos ni sustituir binarios sin verificar.

## 3. Compilar la aplicación con PyInstaller

Desde la raíz del repositorio, utilizando el mismo intérprete del entorno:

```powershell
 .\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean SmartCrop_Store.spec
```

La salida esperada es `dist\SmartCrop\SmartCrop.exe` y `dist\SmartCrop\_internal\`. El archivo `.spec` incluye `collect_all('torch')`, `collect_all('torchvision')` y `collect_all('pi_heif')` y empaqueta recursos, avisos y Real-ESRGAN. **Revisar los avisos de PyInstaller sobre imports faltantes y comprobar el funcionamiento antes de empaquetar**.

### Particularidad de VCOMP140.DLL

En la distribución tradicional se observó `dist\SmartCrop\_internal\VCOMP140.DLL` versión `14.44.35211.0`, SHA-256 `55ABA23CDCD6484FBB06F4155B8CA75ADFCE7A881F10AFD0C49457165E677164`, preparada mediante `preparar_vcomp140.ps1` desde Build Tools. En el contenido final de referencia para Microsoft Store se observó **otra versión y ubicación**: `_internal\shiboken6\VCOMP140.DLL`, versión `14.24.28127.4`, SHA-256 `2407D7152D585A8ECC701454B2903DB3B1ABACA31B4288AE4FBF905F06D5A0F1`, con firma válida.

**No sustituir automáticamente una por otra.** Verificar cuál requiere la compilación concreta y las condiciones de redistribución de Microsoft. El script `preparar_vcomp140.ps1` existente usa rutas absolutas locales; no es un paso universal reproducible.

## 4. Preparar la estructura MSIX

El paquete certificado de referencia se preparó con esta estructura:

```text
Package_Final/
  AppxManifest.xml
  SmartCrop.exe
  _internal/
  Assets/
```

El manifiesto de referencia declara:

- `Identity Name="eskimal.SmartCropAI"`, `Publisher="CN=67244E36-ACAE-4A70-9471-D2D67FACCA7B"`, `Version="1.0.1.0"`, `ProcessorArchitecture="x64"`.
- `Windows.Desktop`, mínimo `10.0.19041.0`.
- `EntryPoint="Windows.FullTrustApplication"`, `RuntimeBehavior="packagedClassicApp"`, `TrustLevel="mediumIL"` y `runFullTrust`.
- Recursos `es-AR` y `en-US`.
- Archivos gráficos del manifiesto dentro de `Assets/`.

El manifiesto original **no forma parte de los archivos del repositorio cuya presencia se ha confirmado**. Para generar un nuevo MSIX se necesita una copia legítima del manifiesto y de los recursos gráficos. No se deben inferir estos archivos a partir del nombre de la aplicación.

## 5. Empaquetar un MSIX nuevo, sin firmar

El script adjunto `build_store_msix.ps1` **no compila Python**: toma una distribución PyInstaller ya generada y un directorio de plantilla que contiene `AppxManifest.xml` y `Assets/`, valida entradas y genera un MSIX nuevo **sin firma** mediante MakeAppx.

Ejemplo con una plantilla local revisada:

```powershell
 .\build_store_msix.ps1 -AppDir '.\dist\SmartCrop' -TemplateDir 'C:\SmartCrop_Test\MSIX_Store\Package_Final' -OutputDir 'C:\SmartCrop_Test\MSIX_Rebuild_Prueba'
```

El script copia **solo** `AppxManifest.xml` y `Assets/` de la plantilla; copia `SmartCrop.exe` y `_internal/` de `AppDir`. No altera `Package_Final` ni el MSIX certificado. El paquete resultante puede conservar la identidad y versión del manifiesto de referencia: **no instalarlo junto con la versión publicada, ni distribuirlo como actualización**, sin revisar identidad, versión, firma y titularidad.

La salida sin firma sirve para inspección técnica; **no está lista para instalarse o publicarse en Microsoft Store**. La firma, la versión, la reserva de identidad y el flujo de envío a Partner Center requieren un procedimiento independiente.

## 6. Verificaciones necesarias

1. Confirmar que `SmartCrop.exe` abre y permite importar, recortar, mover, exportar y usar la mejora IA en un entorno de prueba.
2. Inspeccionar la presencia y licencias de modelos, Real-ESRGAN, Qt, PySide6, Shiboken6 y dependencias transitivas.
3. Comparar el inventario de DLL y plugins Qt de la nueva compilación con `QT_LGPL_COMPLIANCE.md` y `QT_SOURCE_CODE.md`.
4. Inspeccionar `AppxManifest.xml` y los recursos gráficos; validar el paquete con herramientas de Windows SDK.
5. Probar el paquete en un entorno aislado con la firma y el mecanismo de instalación adecuados.
6. Registrar versiones, hashes y comandos reales del build; no declarar reproducibilidad completa sin esta prueba.

## 7. Código fuente de Qt, modificaciones y obligaciones de licencia

Las fuentes oficiales verificadas para **Qt Base 6.11.2**, **Qt SVG 6.11.2** y **Qt for Python/PySide6/Shiboken6 6.11.2**, con hashes, están en `QT_SOURCE_CODE.md`. `QT_LGPL_COMPLIANCE.md` registra una prueba funcional de reemplazo de `Qt6Core.dll` **realmente modificada** en una distribución tradicional PyInstaller `onedir`; también documenta el entorno MSVC/CMake/Ninja y las limitaciones de esa prueba.

**La prueba de reemplazo del EXE tradicional no demuestra que el MSIX instalado permita reemplazar y ejecutar bibliotecas Qt modificadas.** Los archivos de instalación MSIX están sujetos a integridad y restricciones de modificación. Quedan pendientes el mecanismo verificable para usar bibliotecas LGPL modificadas con la distribución Store, la oferta del código fuente correspondiente y materiales de compilación necesarios, los avisos y licencias de cada módulo/plugin, y una revisión legal apropiada. **No considerar este documento autorización para publicar.**

También queda pendiente la revisión de **AGPL-3.0 y Ultralytics**, así como de las condiciones aplicables al código propio, los pesos/modelos, Real-ESRGAN y demás componentes. La certificación técnica de Microsoft Store no sustituye esa revisión.

## 8. Referencias del repositorio

- `README.md`
- `requirements.txt`
- `SmartCrop_Store.spec`
- `preparar_realesrgan.ps1`
- `preparar_vcomp140.ps1`
- `QT_LGPL_COMPLIANCE.md`
- `QT_SOURCE_CODE.md`
- `THIRD_PARTY_NOTICES.md`
