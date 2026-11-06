# SmartCrop AI — Compilación desde el código fuente (Windows / Microsoft Store)

**Estado:** empaquetado MSIX sin firma validado con la nueva plantilla pública y una compilación PyInstaller preexistente; **pendiente de validación integral en un entorno limpio**. No se garantiza que el resultado sea idéntico, byte por byte, al MSIX certificado `1.0.1.0`. Este documento **no acredita cumplimiento de LGPL, AGPL ni de otras licencias**.

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

El manifiesto de referencia está disponible en `MSIX_Template/AppxManifest.xml`, copiado desde `Package_Final` y comparado mediante SHA-256: `9606C76D517AF33A02EAF82774094EEC4D672C08C551FEF7FBB804AE0D03DF65` (ambas copias coinciden). Los recursos gráficos se mantienen en `Assets/` del repositorio, **sin duplicarlos** dentro de `MSIX_Template/`. Se compararon los ocho archivos de `Assets/` con los del paquete final y todos coincidieron por hash.

La identidad y el editor del manifiesto corresponden al paquete de referencia de SmartCrop AI. Una reconstrucción independiente **no debe presentarse como una actualización oficial ni distribuirse con esa identidad sin la autorización y el proceso de firma correspondientes**.

## 5. Empaquetar un MSIX nuevo, sin firmar

El script `build_store_msix.ps1` **no compila Python**: toma una distribución PyInstaller ya generada, el manifiesto de `TemplateDir` y los recursos de `AssetsDir`, valida entradas y genera un MSIX nuevo **sin firma** mediante MakeAppx. Si se omite `AssetsDir`, busca `Assets/` dentro de `TemplateDir` (compatibilidad anterior) o en la carpeta hermana de `MSIX_Template/`.

Ejemplo con los archivos del repositorio (usar una carpeta de salida nueva):

```powershell
 powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\build_store_msix.ps1' -AppDir '.\dist\SmartCrop' -TemplateDir '.\MSIX_Template' -AssetsDir '.\Assets' -OutputDir 'C:\SmartCrop_Test\MSIX_Rebuild_Prueba'
```

El script copia `AppxManifest.xml` de `TemplateDir`, `Assets/` de `AssetsDir` y `SmartCrop.exe` y `_internal/` de `AppDir`. No altera `Package_Final` ni el MSIX certificado. El paquete resultante puede conservar la identidad y versión del manifiesto de referencia: **no instalarlo junto con la versión publicada, ni distribuirlo como actualización**, sin revisar identidad, versión, firma y titularidad.

### Prueba efectuada el 6 de noviembre de 2026

Se ejecutó el script actualizado con `-AppDir '.\dist_store_taskbar\SmartCrop'`, `-TemplateDir '.\MSIX_Template'`, `-AssetsDir '.\Assets'` y `-OutputDir 'C:\SmartCrop_Test\MSIX_Rebuild_NuevaPlantilla'`. **No se recompiló la aplicación**: se reutilizó la compilación PyInstaller previamente comprobada. MakeAppx informó `Package creation succeeded` y generó `SmartCropAI_Rebuild_Unsigned.msix`.

SHA-256 del MSIX de prueba: `18C5E411E0CBCE2AE8E46E4C50CA01E16ECB63864C7FE93D6780564DE7EDCB9E`.

Se inspeccionó el contenido mediante `tar -tf` y se verificó la presencia de `AppxManifest.xml`, `SmartCrop.exe`, `_internal/PySide6/Qt6Core.dll`, `_internal/yolo11n.pt` y `_internal/realesrgan-ncnn-vulkan.exe`. **Esta prueba valida el empaquetado y la presencia de esos archivos, no la instalación del MSIX, su ejecución como aplicación instalada ni una reconstrucción limpia desde fuentes.**

La salida sin firma sirve para inspección técnica; **no está lista para instalarse o publicarse en Microsoft Store**. La firma, la versión, la reserva de identidad y el flujo de envío a Partner Center requieren un procedimiento independiente.

## 6. Verificaciones necesarias

1. Confirmar que `SmartCrop.exe` abre y permite importar, recortar, mover, exportar y usar la mejora IA en un entorno de prueba.
2. Inspeccionar la presencia y licencias de modelos, Real-ESRGAN, Qt, PySide6, Shiboken6 y dependencias transitivas.
3. Comparar el inventario de DLL y plugins Qt de la nueva compilación con `QT_LGPL_COMPLIANCE.md` y `QT_SOURCE_CODE.md`.
4. Inspeccionar `AppxManifest.xml` y los recursos gráficos; validar el paquete con herramientas de Windows SDK.
5. Probar el paquete en un entorno aislado con la firma y el mecanismo de instalación adecuados.
6. Registrar versiones, hashes y comandos reales del build; no declarar reproducibilidad completa sin esta prueba.

## 7. Código fuente de Qt, modificaciones y obligaciones de licencia

Las fuentes oficiales verificadas para **Qt Base 6.11.2**, **Qt SVG 6.11.2** y **Qt for Python/PySide6/Shiboken6 6.11.2**, con hashes, están en `QT_SOURCE_CODE.md`. `QT_LGPL_COMPLIANCE.md` registra una prueba funcional de reemplazo de `Qt6Core.dll` **realmente modificada** en una copia independiente de la distribución PyInstaller utilizada como base de Store, fuera de la instalación MSIX; también documenta el entorno MSVC/CMake/Ninja y las limitaciones de esa prueba.

**La prueba de reemplazo en una copia PyInstaller fuera de MSIX no demuestra que el MSIX instalado permita reemplazar y ejecutar bibliotecas Qt modificadas.** Los archivos de instalación MSIX están sujetos a integridad y restricciones de modificación. Quedan pendientes el mecanismo verificable para usar bibliotecas LGPL modificadas con la distribución Store, la oferta del código fuente correspondiente y materiales de compilación necesarios, los avisos y licencias de cada módulo/plugin, y una revisión legal apropiada. **No considerar este documento autorización para publicar.**

También queda pendiente la revisión de **AGPL-3.0 y Ultralytics**, así como de las condiciones aplicables al código propio, los pesos/modelos, Real-ESRGAN y demás componentes. La certificación técnica de Microsoft Store no sustituye esa revisión.

## 8. Referencias del repositorio

- `README.md`
- `requirements.txt`
- `SmartCrop_Store.spec`
- `MSIX_Template/AppxManifest.xml`
- `Assets/`
- `build_store_msix.ps1`
- `preparar_realesrgan.ps1`
- `preparar_vcomp140.ps1`
- `QT_LGPL_COMPLIANCE.md`
- `QT_SOURCE_CODE.md`
- `THIRD_PARTY_NOTICES.md`
