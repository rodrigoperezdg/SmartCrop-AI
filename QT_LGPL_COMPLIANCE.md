# Qt / PySide6 / Shiboken6 — información de licencias de SmartCrop AI

**Estado (25 de octubre de 2026):** inventario y pruebas técnicas de la versión 1.0.0, con obligaciones legales todavía pendientes. **No constituye una certificación de cumplimiento legal ni autoriza por sí solo la publicación.**

## Versiones identificadas

- Qt: **6.11.2**, confirmado por `qVersion()` y por la información de versión de `Qt6Core.dll` de la compilación.
- PySide6, PySide6_Essentials y PySide6_Addons: **6.11.2**, según `pip show` en el entorno de compilación.
- Shiboken6: **6.11.2**, según `pip show` en el entorno de compilación.
- Los cuatro paquetes declaran `LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only` en sus metadatos. La elección de LGPL-3.0 requiere respetar sus condiciones; no debe extrapolarse automáticamente a todos los módulos y binarios de Qt.

## Archivos de Qt observados en la compilación de prueba

Bibliotecas Qt (`_internal/PySide6/`):

- `Qt6Core.dll`
- `Qt6Gui.dll`
- `Qt6Network.dll`
- `Qt6OpenGL.dll`
- `Qt6Svg.dll`
- `Qt6Widgets.dll`

Extensiones de PySide6 (`_internal/PySide6/`):

- `QtCore.pyd`
- `QtGui.pyd`
- `QtWidgets.pyd`

Componentes Shiboken6 (`_internal/shiboken6/`):

- `Shiboken.pyd`
- `shiboken6.abi3.dll`

Plugins Qt (`_internal/PySide6/plugins/`):

- `generic/qtuiotouchplugin.dll`
- `iconengines/qsvgicon.dll`
- `imageformats/qgif.dll`
- `imageformats/qicns.dll`
- `imageformats/qico.dll`
- `imageformats/qjpeg.dll`
- `imageformats/qsvg.dll`
- `imageformats/qtga.dll`
- `imageformats/qtiff.dll`
- `imageformats/qwbmp.dll`
- `imageformats/qwebp.dll`
- `platforms/qdirect2d.dll`
- `platforms/qminimal.dll`
- `platforms/qoffscreen.dll`
- `platforms/qwindows.dll`
- `styles/qmodernwindowsstyle.dll`

**Nota:** posteriormente se volvió a inventariar `C:\SmartCrop_Test\dist\SmartCrop` y se observaron las seis DLL Qt, las tres extensiones PySide6, los dos componentes Shiboken6 y los 16 plugins enumerados. Es necesario volver a comprobar el paquete que se distribuya finalmente si se recompila o cambia el contenido.

## Licencias y fuentes

Qt, Qt for Python (PySide6) y Shiboken6 incluyen componentes con distintas condiciones de licencia, que pueden variar según el módulo y la distribución. Es necesario conservar los avisos de copyright y los textos de licencia correspondientes a los binarios efectivamente distribuidos.

Referencias oficiales:

- Licencias de Qt for Python: https://doc.qt.io/qtforpython-6/licenses.html
- Obligaciones LGPL de Qt: https://www.qt.io/development/open-source-lgpl-obligations
- Repositorio de Qt Base: https://code.qt.io/cgit/qt/qtbase.git/
- Repositorio de Qt SVG: https://code.qt.io/cgit/qt/qtsvg.git/
- Repositorio de Qt for Python (PySide6 y Shiboken6): https://code.qt.io/cgit/pyside/pyside-setup.git/
- Descargas de fuentes Qt 6.11.2: https://download.qt.io/official_releases/qt/6.11/6.11.2/submodules/

**Textos y avisos reunidos:** en el proyecto existen `LICENSE-LGPL-3.0.txt`, `LICENSE-GPL-3.0.txt`, `THIRD_PARTY_NOTICES.md` y `LEGAL_TERCEROS/`. Se comprobó que la compilación nueva incluye las licencias principales y 115 archivos de `LEGAL_TERCEROS/`; estos 115 archivos corresponden a otras dependencias de Python y **no reemplazan** una auditoría de avisos y fuentes de Qt.

**Fuentes oficiales descargadas y verificadas (25/10/2026):**

| Paquete | Archivo | SHA-256 verificado | Tamaño aproximado |
|---|---|---|---:|
| Qt Base 6.11.2 | `qtbase-everywhere-src-6.11.2.tar.xz` | `5B2E00ECCAF5A4D8C14134FFA0EA8DFD0A35AE1FFC7F8D87FA4305A1ED23CF22` | 48,24 MiB |
| Qt SVG 6.11.2 | `qtsvg-everywhere-src-6.11.2.tar.xz` | `D594337FECA84C26FB67FE87B85E6A5C12FDA404B611D905F9D138210C311876` | 2,23 MiB |
| Qt for Python / PySide6 / Shiboken6 6.11.2 | `pyside-setup-everywhere-src-6.11.2.tar.xz` | `CBA47EFBAAD1BEDD529725CBC14E21F156C7A19366F07B3EDFBB076FFD7AFDF8` | 17,22 MiB |

Los archivos se guardaron localmente en `una carpeta local de descarga de fuentes Qt`. Los hashes locales coincidieron con los valores oficiales consultados. Fuente Qt for Python: https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/ . El inventario del paquete `C:\SmartCrop_Test\dist\SmartCrop` identificó las seis DLL Qt, tres extensiones PySide6, dos componentes Shiboken6 y los 16 plugins listados arriba. Según sus nombres y módulos, esos componentes corresponden a Qt Base, Qt SVG y Qt for Python; esto **no sustituye** la revisión de licencias y fuentes de terceros integrados en cada módulo.

**Pendiente antes de publicar:** preparar la provisión u oferta de código fuente correspondiente a los binarios efectivamente distribuidos (incluidos cambios y configuraciones cuando correspondan), revisar los avisos de copyright y condiciones específicas de cada plugin y dependencia. Conservar un enlace no satisface necesariamente todas las obligaciones.

## Uso de bibliotecas modificadas en la versión tradicional (EXE)

La distribución tradicional de SmartCrop AI creada con PyInstaller en modo `onedir` coloca las DLL de Qt en una carpeta separada del ejecutable. Una persona que desee utilizar una versión modificada de una biblioteca Qt puede, en principio:

1. Obtener el código fuente correspondiente a la versión de Qt utilizada.
2. Compilar una versión binariamente compatible de la biblioteca para Windows x64, utilizando una configuración compatible.
3. Hacer una copia de seguridad de la instalación de SmartCrop y reemplazar la DLL correspondiente en `_internal/PySide6/` con la aplicación cerrada.
4. Ejecutar SmartCrop y verificar su funcionamiento. También podrían requerirse plugins o dependencias compatibles.

### Prueba inicial: reemplazo por una DLL idéntica

- Compilación de prueba: `C:\SmartCrop_Test\dist\SmartCrop\SmartCrop.exe`.
- Copia inicial: `C:\SmartCrop_Test\SmartCrop_QtTest\SmartCrop.exe`.
- Se sustituyó `Qt6Svg.dll` por un archivo de PySide6 6.11.2 con el **mismo** SHA-256 (`1EAC8F7415B311A88CB3CB4E25C3098D0E059C24C831FBBB13F43A80F0DF06B7`); SmartCrop funcionó. Esta prueba por sí sola no demostraba uso de Qt modificado.

### Prueba posterior: Qt Base recompilado y realmente modificado (25/10/2026)

**Entorno:** Windows x64; Visual Studio Build Tools 2022, MSVC 19.44.35220, CMake 3.31.6, Ninja 1.12.1. Los ejecutables no estaban en el `PATH` inicial, pero se encontraron dentro de Visual Studio y se activaron mediante `vcvars64.bat`. El SDK Qt convencional no estaba instalado en las rutas revisadas.

**Fuentes y compilación:** se extrajo `qtbase-everywhere-src-6.11.2.tar.xz` en `C:\SmartCrop_Test\QtBuild\qtbase-everywhere-src-6.11.2`. Se configuró con CMake/Ninja en `C:\SmartCrop_Test\QtBuild\build`, tipo `Release`, prefijo de instalación `C:\SmartCrop_Test\QtBuild\install`, pruebas y ejemplos deshabilitados. CMake terminó con código 0; la compilación inicial de Qt Base completó 1.896 tareas con código 0.

**Sustitución de bibliotecas:** se creó `C:\SmartCrop_Test\SmartCrop_QtCompilado` a partir de la distribución PyInstaller. Se respaldaron las DLL originales y se sustituyeron `Qt6Core.dll`, `Qt6Gui.dll`, `Qt6Network.dll`, `Qt6OpenGL.dll` y `Qt6Widgets.dll` por las recompiladas. Los cinco hashes de destino coincidieron con los de origen. El primer inicio falló con «no Qt platform plugin could be initialized» al utilizar el plugin `qwindows.dll` original de PySide6. Se respaldó y sustituyó también `plugins/platforms/qwindows.dll` por el compilado junto con Qt Base; su hash de destino coincidió con el origen. El usuario confirmó que SmartCrop inició y funcionó con esta combinación.

**Modificación real:** se hizo copia de seguridad de `src/corelib/global/qversiontagging.cpp` y se agregó al final del archivo el siguiente símbolo exportado, sin alterar los símbolos existentes de versión:

```cpp
// SmartCrop AI - LGPL replacement test.
// This marker does not change Qt's public interfaces or version symbols.
extern "C" __declspec(dllexport) const char smartcrop_qt_lgpl_test_marker[] =
    "SMARTCROP_QT_LGPL_TEST_2026";
```

Se recompiló Qt Base con Ninja: finalizó con código 0 y actualizó `Qt6Core.dll`. La versión siguió siendo **6.11.2.0**. SHA-256 antes de modificar: `E8DE8237E76A207F274516837D71F94734DA3FC598814B30272CD91976EB9A7C`; después: `078E92FD47B7B16F7678ABFD8AE485D47E7D3B3190CFB89AC6827C703E36EE6D`. `dumpbin /exports` confirmó la exportación de `smartcrop_qt_lgpl_test_marker`.

**Prueba funcional final:** se copió exclusivamente la `Qt6Core.dll` modificada a la copia aislada `SmartCrop_QtCompilado` (con las otras DLL y `qwindows.dll` compatibles ya recompiladas). Se comprobó que los hashes coincidieran y el usuario confirmó que **SmartCrop abrió y exportó correctamente** con la DLL modificada.

**Conclusión y límites:** existe evidencia práctica de sustitución y funcionamiento de **una** biblioteca Qt modificada en la distribución tradicional tipo `onedir` bajo esta configuración. No se probó cualquier modificación posible, otros equipos, todos los plugins ni una instalación realizada por Inno Setup con este reemplazo. Esta prueba **no certifica** por sí sola cumplimiento LGPL; aún hay que ofrecer fuentes, instrucciones reproducibles y avisos adecuados, y revisar las restricciones de distribución y MSIX. La DLL de prueba modificada no se incorporó al instalador de producción.

## Advertencia sobre MSIX y Microsoft Store

Los paquetes MSIX se firman y su instalación está sujeta a mecanismos de integridad. No se ha demostrado que un usuario pueda reemplazar las bibliotecas Qt dentro de un SmartCrop instalado mediante MSIX y seguir ejecutándolo. **La existencia de un instalador EXE alternativo no resuelve automáticamente las obligaciones de una distribución MSIX separada.**

**Estado:** compatibilidad de la distribución MSIX con LGPL-3.0 **sin resolver**. No publicar como conforme ni enviar a certificación hasta contar con una solución técnicamente comprobada y una revisión legal adecuada. Las opciones a evaluar incluyen una vía documentada para instalar y ejecutar una versión modificada, un esquema de distribución distinto o licencias comerciales cuando corresponda.

## Estado de la compilación y el instalador 1.0.0

- PyInstaller finalizó sin errores y se comprobó la presencia de `SmartCrop.exe`, `yolo11n.pt`, `realesrgan-ncnn-vulkan.exe`, `realesrgan-x4plus.bin`, `realesrgan-x4plus.param`, `LICENSE-GPL-3.0.txt` y `LEGAL_TERCEROS/`.
- Los recuentos de archivos legales originales y compilados coincidieron: **115 archivos**.
- El usuario probó satisfactoriamente importación, recorte, movimiento manual, exportación y mejora con IA.
- Inno Setup generó el instalador 1.0.0; la instalación, apertura desde menú Inicio, uso y desinstalación fueron probados. Tras desinstalar, `Test-Path "$env:LOCALAPPDATA\Programs\SmartCrop AI"` devolvió `False`.
- **Alcance:** son pruebas funcionales de ese equipo, no pruebas exhaustivas en otros Windows ni un dictamen de cumplimiento de licencias.

## Lista de verificación previa a publicación

- [x] Inventariar Qt, plugins, PySide6 y Shiboken6 en la compilación de prueba (6 DLL Qt, 3 extensiones PySide6, 2 componentes Shiboken6, 16 plugins). Repetir si cambia el paquete final.
- [ ] Verificar licencias exactas y avisos de copyright de cada componente incluido.
- [x] Incluir textos principales y carpeta de avisos recopilados en la compilación 1.0.0 (presencia comprobada).
- [ ] Auditar suficiencia de los avisos de Qt y proporcionar el código fuente correspondiente conforme a las licencias aplicables.
- [ ] Publicar instrucciones reproducibles de sustitución y configuraciones de compilación, y documentar parches/cambios exigibles (esta prueba ya quedó registrada).
- [x] Probar la sustitución física de una DLL Qt por otra idéntica en una copia aislada (no demuestra compatibilidad con DLL modificada).
- [x] Probar una biblioteca Qt genuinamente modificada en una copia aislada `onedir`: `Qt6Core.dll` modificada, exportación comprobada y SmartCrop funcional. Pendiente documentar procedimiento para usuarios de la versión instalada.
- [ ] Resolver por separado la posibilidad de usar bibliotecas modificadas en la distribución MSIX.
- [ ] Revisar los términos de Microsoft Store y las obligaciones de AGPL-3.0 del código de SmartCrop y Ultralytics.
