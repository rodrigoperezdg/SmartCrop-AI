# SmartCrop AI 1.0.0 / Store 1.0.1.0 — Fuentes de Qt / Qt for Python

Este documento identifica los archivos fuente oficiales correspondientes a los componentes Qt detectados en la compilación tradicional 1.0.0 y en la compilación Store 1.0.1.0 de SmartCrop AI. **No constituye, por sí solo, una certificación de cumplimiento de LGPL.**

## Versiones y archivos fuente

| Componente | Archivo fuente | SHA-256 (comprobado contra el valor publicado por Qt) |
|---|---|---|
| Qt Base 6.11.2 | `qtbase-everywhere-src-6.11.2.tar.xz` | `5b2e00eccaf5a4d8c14134ffa0ea8dfd0a35ae1ffc7f8d87fa4305a1ed23cf22` |
| Qt SVG 6.11.2 | `qtsvg-everywhere-src-6.11.2.tar.xz` | `d594337feca84c26fb67fe87b85e6a5c12fda404b611d905f9d138210c311876` |
| Qt for Python (PySide6/Shiboken6) 6.11.2 | `pyside-setup-everywhere-src-6.11.2.tar.xz` | `cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8` |

Fuentes oficiales:

- Qt Base: https://download.qt.io/official_releases/qt/6.11/6.11.2/submodules/qtbase-everywhere-src-6.11.2.tar.xz
- Qt SVG: https://download.qt.io/official_releases/qt/6.11/6.11.2/submodules/qtsvg-everywhere-src-6.11.2.tar.xz
- Qt for Python: https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/pyside-setup-everywhere-src-6.11.2.tar.xz

Los archivos se descargaron en la máquina de desarrollo en `Downloads\SmartCrop_Fuentes_Qt` y se verificaron los tres hashes frente a los publicados por Qt (Qt Base y Qt SVG mediante archivos `.sha256`; Qt for Python mediante valor oficial previamente comprobado).

## Componentes identificados en la distribución PyInstaller

**Qt Base:** `Qt6Core.dll`, `Qt6Gui.dll`, `Qt6Network.dll`, `Qt6OpenGL.dll`, `Qt6Widgets.dll`.

**Qt SVG:** `Qt6Svg.dll`.

**Qt for Python:** `QtCore.pyd`, `QtGui.pyd`, `QtWidgets.pyd`, `Shiboken.pyd`, `shiboken6.abi3.dll`.

**Plugins de Qt Base (14):** `qtuiotouchplugin.dll`, `qgif.dll`, `qicns.dll`, `qico.dll`, `qjpeg.dll`, `qtga.dll`, `qtiff.dll`, `qwbmp.dll`, `qwebp.dll`, `qdirect2d.dll`, `qminimal.dll`, `qoffscreen.dll`, `qwindows.dll`, `qmodernwindowsstyle.dll`.

**Plugins de Qt SVG (2):** `qsvgicon.dll`, `qsvg.dll`.

Este inventario se basa en los nombres de archivos reportados en `C:\SmartCrop_Test\dist\SmartCrop\_internal`. No sustituye una auditoría de dependencias transitivas, código modificado, opciones de compilación ni licencias de terceros incluidas en los paquetes.

## Verificación adicional de Store (5/11/2026)

En `C:\SmartCrop_Test\MSIX_Store\Package_Final`, preparado para el MSIX Store 1.0.1.0, se verificó que `SmartCrop.exe` coincide por SHA-256 con `dist_store_taskbar/SmartCrop/SmartCrop.exe`: `EFEE83E00A6896D6C7C3248D7512D7DFADFFA35C36E4F35CB53DC7C12D51F925`. También coincidieron por hash las seis DLL principales de Qt enumeradas anteriormente.

La `Qt6Core.dll` de esa compilación se sustituyó en **una copia independiente, no instalada mediante MSIX**, por una versión 6.11.2 recompilada con una modificación real y SHA-256 `078E92FD47B7B16F7678ABFD8AE485D47E7D3B3190CFB89AC6827C703E36EE6D`. SmartCrop abrió, importó, recortó y exportó una imagen correctamente. Los pasos y limitaciones están documentados en `QT_LGPL_COMPLIANCE.md`.

Los tres archivos fuente `.tar.xz` enumerados arriba seguían presentes en `Downloads\SmartCrop_Fuentes_Qt` el 5/11/2026. Se comprobó su existencia y tamaño, **no se recalcularon sus hashes ese día**. La verificación SHA-256 original se mantiene documentada.

El paquete Store 1.0.1.0 superó la certificación técnica de Microsoft y está pendiente de publicación. **La certificación no acredita cumplimiento LGPL**. El mecanismo de reemplazo de Qt en una instalación MSIX protegida sigue sin comprobarse. Tampoco se ha demostrado una reconstrucción binariamente idéntica del MSIX certificado.

## Pendientes antes de distribuir

1. Documentar para destinatarios el mecanismo de sustitución en distribución independiente, ya probado con una modificación efectiva; evaluar por separado su suficiencia jurídica para cada modalidad de distribución.
2. Comprobar obligaciones concretas de LGPL y otras licencias aplicables a cada biblioteca y plugin, incluidos avisos y texto de licencia, y la disponibilidad del código fuente correspondiente bajo condiciones apropiadas. Los enlaces externos por sí solos pueden no satisfacer todas las obligaciones.
3. Comprobar si se necesitan instrucciones de compilación, opciones/configuración y materiales adicionales para reconstruir los componentes efectivamente distribuidos.
4. Resolver las restricciones de integridad, actualización y reemplazo de DLLs de una instalación MSIX de Microsoft Store; la prueba `onedir` no las resuelve.
5. Revisar las licencias de las demás dependencias (Ultralytics/YOLO, Real-ESRGAN y pesos, PyTorch, OpenCV, etc.).
6. Actualizar este documento si cambian versiones, archivos o método de empaquetado, e incluirlo en la distribución final.

**Estado:** inventario y archivos fuente localizados/verificados; cumplimiento de distribución aún pendiente de validar.
