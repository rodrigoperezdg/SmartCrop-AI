# SmartCrop AI — Reconstrucción y sustitución de Qt 6.11.2

**Alcance:** Windows x64, distribución independiente PyInstaller `onedir`. Guía basada en pruebas del 25/10 y 5/11/2026. **No acredita cumplimiento LGPL-3.0 en Microsoft Store ni permite concluir que se puedan sustituir DLL dentro de un MSIX instalado.**

## Fuentes oficiales

| Componente | Archivo | SHA-256 verificado |
|---|---|---|
| Qt Base 6.11.2 | `qtbase-everywhere-src-6.11.2.tar.xz` | `5b2e00eccaf5a4d8c14134ffa0ea8dfd0a35ae1ffc7f8d87fa4305a1ed23cf22` |
| Qt SVG 6.11.2 | `qtsvg-everywhere-src-6.11.2.tar.xz` | `d594337feca84c26fb67fe87b85e6a5c12fda404b611d905f9d138210c311876` |
| Qt for Python 6.11.2 | `pyside-setup-everywhere-src-6.11.2.tar.xz` | `cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8` |

Enlaces oficiales:

- https://download.qt.io/official_releases/qt/6.11/6.11.2/submodules/qtbase-everywhere-src-6.11.2.tar.xz
- https://download.qt.io/official_releases/qt/6.11/6.11.2/submodules/qtsvg-everywhere-src-6.11.2.tar.xz
- https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/pyside-setup-everywhere-src-6.11.2.tar.xz

Verificar los archivos descargados con `Get-FileHash -Algorithm SHA256`. Consultar también `QT_SOURCE_CODE.md`. Los enlaces externos por sí solos no demuestran el cumplimiento de las obligaciones de entrega de fuentes.

## Entorno de compilación observado

Windows x64; Visual Studio Build Tools 2022; herramientas MSVC 14.44.35207, compilador documentado 19.44.35220; CMake 3.31.6; Ninja 1.12.1. Se habilitó el entorno con `vcvars64.bat`.

Valores recuperados de `CMakeCache.txt`: `CMAKE_GENERATOR=Ninja`, `CMAKE_BUILD_TYPE=Release`, `BUILD_SHARED_LIBS=ON`, `QT_BUILD_TESTS=OFF`, `QT_BUILD_EXAMPLES=OFF`; características `gui`, `network`, `opengl`, `widgets` y `shared` activadas.

Rutas locales usadas en la prueba:

```text
C:\SmartCrop_Test\QtBuild\qtbase-everywhere-src-6.11.2
C:\SmartCrop_Test\QtBuild\build
C:\SmartCrop_Test\QtBuild\install
```

**Ejemplo orientativo**, reconstruido a partir de esos valores, **no transcripción de la línea original de CMake ni receta íntegramente validada desde cero**:

```powershell
cmake -S 'C:\SmartCrop_Test\QtBuild\qtbase-everywhere-src-6.11.2' -B 'C:\SmartCrop_Test\QtBuild\build' -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX='C:\SmartCrop_Test\QtBuild\install'
cmake --build 'C:\SmartCrop_Test\QtBuild\build' --parallel
```

Comprobar las opciones aceptadas, la configuración final y los artefactos generados. La prueba recompiló Qt Base; no acredita reconstrucción completa de Qt SVG ni de PySide6/Shiboken6.

## Modificación real probada

Se respaldó `src/corelib/global/qversiontagging.cpp` y se añadió:

```cpp
// SmartCrop AI - LGPL replacement test.
// This marker does not change Qt's public interfaces or version symbols.
extern "C" __declspec(dllexport) const char smartcrop_qt_lgpl_test_marker[] =
    "SMARTCROP_QT_LGPL_TEST_2026";
```

Después de recompilar con Ninja se verificó el símbolo mediante `dumpbin /exports`. Hash SHA-256 de la `Qt6Core.dll` anterior: `E8DE8237E76A207F274516837D71F94734DA3FC598814B30272CD91976EB9A7C`; de la modificada: `078E92FD47B7B16F7678ABFD8AE485D47E7D3B3190CFB89AC6827C703E36EE6D`. Son hashes de artefactos concretos, no valores universales.

## Sustitución en copia independiente

1. Obtener una distribución `onedir` de SmartCrop AI, o reconstruirla según `BUILD_STORE_FROM_SOURCE.md`.
2. Copiar **toda la carpeta** a un directorio de prueba con permisos de escritura. Cerrar la aplicación y respaldar los archivos originales. **No modificar el MSIX certificado ni la carpeta WindowsApps.**
3. En la primera prueba se sustituyeron por artefactos recompilados compatibles de Qt Base:

```text
_internal\PySide6\Qt6Core.dll
_internal\PySide6\Qt6Gui.dll
_internal\PySide6\Qt6Network.dll
_internal\PySide6\Qt6OpenGL.dll
_internal\PySide6\Qt6Widgets.dll
_internal\PySide6\plugins\platforms\qwindows.dll
```

4. Al principio SmartCrop no inició porque se había conservado el `qwindows.dll` original. La sustitución por el plugin compilado junto con Qt Base resolvió el problema. **No mezclar arbitrariamente DLL y plugins de compilaciones distintas.**
5. Una vez preparada esa combinación compatible, se reemplazó **solo** `Qt6Core.dll` por la versión realmente modificada. SmartCrop abrió y exportó correctamente.
6. Comparar hashes de los archivos copiados con `Get-FileHash` y probar importación, recorte y exportación.

**Prueba adicional del 5/11/2026:** una copia independiente del ejecutable exacto empleado para Store 1.0.1.0 (`SmartCrop.exe` SHA-256 `EFEE83E00A6896D6C7C3248D7512D7DFADFFA35C36E4F35CB53DC7C12D51F925`) funcionó con `Qt6Core.dll` modificada: abrió, importó, recortó y exportó. **No se sustituyó la DLL dentro de una instalación MSIX.**

En la reconstrucción limpia posterior, las seis DLL principales de Qt coincidieron por SHA-256 con las del paquete certificado; los ejecutables no fueron idénticos: la reconstrucción contenía Python 3.14.7 y el paquete certificado Python 3.14.0.

## Limitaciones y pendientes de licencia

- La certificación técnica de Microsoft Store no acredita cumplimiento LGPL.
- No se ha demostrado un mecanismo para sustituir bibliotecas Qt dentro de la instalación MSIX protegida.
- Una copia independiente modificable y esta guía **no resuelven automáticamente** las obligaciones LGPL-3.0 de la distribución MSIX. Deben revisarse los requisitos concretos de la licencia, los avisos, las fuentes y materiales correspondientes, las condiciones de modificación y depuración y las restricciones de la plataforma.
- Falta la auditoría final de AGPL-3.0/Ultralytics, Real-ESRGAN, modelos, plugins y dependencias transitivas.
- **No presentar el paquete Store como conforme ni publicarlo basándose solamente en esta guía.** Obtener revisión jurídica apropiada.

Documentos relacionados: `QT_SOURCE_CODE.md`, `QT_LGPL_COMPLIANCE.md`, `BUILD_STORE_FROM_SOURCE.md`, `THIRD_PARTY_NOTICES.md`, `LICENSE-LGPL-3.0.txt`.

**Estado:** procedimiento técnico documentado; reproducción integral por terceros y suficiencia jurídica para Store pendientes.
