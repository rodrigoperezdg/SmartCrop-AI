# Componentes de terceros — SmartCrop AI

Este documento identifica los principales componentes de terceros usados por SmartCrop AI. Se basa en el inventario de la compilación de prueba y en las versiones verificadas en el entorno de desarrollo; **no sustituye una auditoría de licencias del paquete final**.

## 1. Ultralytics YOLO

- Componentes: `ultralytics` 8.4.157 y pesos `yolo11n.pt`.
- Proyecto: https://github.com/ultralytics/ultralytics
- Licencia declarada por el paquete y por los metadatos del modelo: **AGPL-3.0**.
- SmartCrop AI también se publica bajo AGPL-3.0.

Antes de publicar, comprobar que el repositorio contiene el código fuente correspondiente a la versión exacta del ejecutable, los avisos pertinentes y las instrucciones necesarias para reconstruirla. La coincidencia de licencias no elimina estas obligaciones.

## 2. Real-ESRGAN NCNN Vulkan, modelos y dependencias históricas

### Ejecutable y modelos

- Ejecutable: `realesrgan-ncnn-vulkan.exe`.
- Proyecto: https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan
- Distribución identificada: `realesrgan-ncnn-vulkan-20220424-windows`.
- Licencia declarada del proyecto del ejecutable: **MIT**. Avisos identificados: Copyright (c) 2021 Xintao Wang; Copyright (c) 2019 nihui.
- Licencias conservadas: `LICENSE-Real-ESRGAN.txt` y `LEGAL_TERCEROS/RealESRGAN_NCNN_2022_LICENSE.txt` (licencia del árbol de código `v0.2.0`).
- SHA-256 del ejecutable local, comparado previamente con la distribución identificada: `07E49F7CBB4EDE01AE4DD4C399D3A7E5846E3D2085C3128EFF881E55CB7B1A0C`.
- Modelo utilizado: `models/realesrgan-x4plus.bin` y `models/realesrgan-x4plus.param`. El archivo `SmartCrop.spec` inspeccionado incluye explícitamente estos dos modelos, no los otros ocho archivos guardados en `models_backup`. **Verificar el contenido efectivo del instalador final**.
- Proyecto de origen del modelo: https://github.com/xinntao/Real-ESRGAN
- Licencia BSD-3-Clause del proyecto original conservada en `LEGAL_TERCEROS/Real-ESRGAN_BSD-3-Clause_LICENSE.txt` (copyright 2021 Xintao Wang). **La licencia del repositorio no acredita por sí sola las condiciones particulares de redistribución de los pesos NCNN `.bin` y `.param`**.

La procedencia de ambos archivos fue comprobada contra el ZIP oficial
realesrgan-ncnn-vulkan-20220424-windows.zip mediante SHA-256:

- realesrgan-x4plus.bin:
  713EE713B0353AFAA27976F0563A64A5043BD70B9BD8936C2E26E25EBCDBCDDF
- realesrgan-x4plus.param:
  35330ECECCEA33B6C397A72548E788D5D53BECEE4734C50B7FADA36E89F10A86

Ambos hashes coinciden exactamente con los archivos de la distribución.
El README_windows.md de ese ZIP enumera expresamente el modelo realesrgan-x4plus.

La licencia BSD-3-Clause del repositorio original no acredita por sí sola
las condiciones particulares de redistribución de los pesos NCNN.
La autorización específica para redistribuir esos pesos permanece pendiente
de confirmación antes de publicar.

### Submódulos identificados en el árbol `v0.2.0`

El árbol Git de `Real-ESRGAN-ncnn-vulkan` en la etiqueta `v0.2.0` referencia:

| Componente | Commit del submódulo | Documentos históricos conservados |
| --- | --- | --- |
| NCNN (`Tencent/ncnn`) | `6125c9f47cd14b589de0521350668cf9d3d37e3c` | `LEGAL_TERCEROS/NCNN_2022_LICENSE.txt` (BSD-3-Clause y avisos de terceros; 6.502 bytes) |
| libwebp (`webmproject/libwebp`) | `8ea81561d2fdd382da60f57958741a7c23a18eb6` | `LEGAL_TERCEROS/libwebp_2022_COPYING.txt` y `LEGAL_TERCEROS/libwebp_2022_PATENTS.txt` |

Se conserva además `LEGAL_TERCEROS/NCNN_BSD-3-Clause_LICENSE.txt`, obtenido de la rama actual de NCNN; **para el análisis histórico tiene prioridad el archivo `NCNN_2022_LICENSE.txt`**. Este último incorpora avisos de terceros, entre ellos archivos matemáticos con licencia zlib y componentes con licencias BSD. La presencia de un aviso en ese documento no demuestra que el componente se haya compilado en el binario Windows.

### Cabeceras del código fuente histórico `v0.2.0`

- `src/stb_image.h` **v2.26**: licencia alternativa MIT o dominio público/Unlicense. Archivo histórico conservado en `LEGAL_TERCEROS/RealESRGAN_2022_stb_image.h.txt`.
- `src/stb_image_write.h` **v1.15**: licencia alternativa MIT o dominio público/Unlicense. Archivo histórico conservado en `LEGAL_TERCEROS/RealESRGAN_2022_stb_image_write.h.txt`.
- Ambos textos ofrecen la alternativa **MIT**, con aviso `Copyright (c) 2017 Sean Barrett`; para los avisos de SmartCrop se documenta esa alternativa y se conserva el texto completo en las cabeceras históricas.
- `src/win32dirent.h`: declara licencia **MIT**, copyright (C) 1998-2019 Toni Ronkko. Cabecera histórica conservada en `LEGAL_TERCEROS/RealESRGAN_2022_win32dirent.h.txt`.

**Alcance de la evidencia:** los commits y las cabeceras corresponden al árbol fuente etiquetado `v0.2.0`. Todavía no se ha demostrado de forma concluyente que el ejecutable `20220424` se compilara exactamente desde ese árbol o con las mismas opciones; revisar también cualquier dependencia enlazada estáticamente y sus avisos antes de declarar cerrado el inventario.

### Dependencias dinámicas observadas en Windows

La inspección de `realesrgan-ncnn-vulkan.exe` mediante `dumpbin /DEPENDENTS` identificó `vulkan-1.dll`, `ole32.dll`, `KERNEL32.dll`, `OLEAUT32.dll` y `VCOMP140.DLL`. Las DLL de Windows y Vulkan identificadas como dependencias **no se consideran automáticamente redistribuidas** por figurar en esta lista; comprobar qué archivos contiene el paquete final. `dumpbin` no enumera todas las bibliotecas enlazadas estáticamente.

## 3. Qt 6.11.2, PySide6 6.11.2 y Shiboken6 6.11.2

- Proyecto y condiciones: https://doc.qt.io/qtforpython-6/licenses.html
- Inventario e instrucciones preliminares: [`QT_LGPL_COMPLIANCE.md`](QT_LGPL_COMPLIANCE.md).
- Texto LGPL-3.0 disponible en el proyecto: [`LICENSE-LGPL-3.0.txt`](LICENSE-LGPL-3.0.txt).

En la compilación de prueba se identificaron:

- DLL de Qt: `Qt6Core`, `Qt6Gui`, `Qt6Network`, `Qt6OpenGL`, `Qt6Svg` y `Qt6Widgets`.
- Módulos de PySide6: `QtCore.pyd`, `QtGui.pyd`, `QtWidgets.pyd`.
- Shiboken6: `Shiboken.pyd`, `shiboken6.abi3.dll`.
- Dieciséis plugins Qt, incluidos los de plataforma, formatos de imagen, iconos SVG, estilos y entrada táctil.

La distribución tradicional permite acceder físicamente a las DLL. Además de pruebas con bibliotecas de idéntico contenido, se realizó una prueba aislada con bibliotecas Qt Base compiladas desde código fuente y el plugin de plataforma correspondiente. Se modificó `qversiontagging.cpp` para exportar el símbolo `smartcrop_qt_lgpl_test_marker`, se recompiló `Qt6Core.dll`, se verificó la presencia del símbolo y el cambio de SHA-256, y la aplicación abrió y exportó correctamente con esa biblioteca modificada en el entorno de prueba. Los detalles se documentan en `QT_LGPL_COMPLIANCE.md`. Esta prueba técnica no demuestra por sí sola el cumplimiento jurídico integral ni la viabilidad de sustitución en MSIX.

**Pendiente:** determinar las licencias exactas de todos los módulos y plugins distribuidos, conservar sus avisos y proporcionar el código fuente correspondiente conforme a las obligaciones aplicables. La distribución MSIX requiere una evaluación independiente sobre la posibilidad efectiva de ejecutar bibliotecas modificadas y las condiciones de Microsoft Store. La presencia del texto LGPL no demuestra cumplimiento completo.

## 4. Bibliotecas y herramientas de Python

Versiones directas documentadas en `requirements.txt`:

- PyTorch 2.14.0 y torchvision 0.29.0.
- OpenCV (`opencv-python`) 4.12.0.88.
- Pillow 12.3.0.
- `pillow-avif-plugin` 1.6.0.
- NumPy 2.2.6.
- `pi-heif` 1.4.0 (su paquete declara licencia BSD-3-Clause).
- PyInstaller 6.22.3 (herramienta de compilación; verificar qué partes suyas se redistribuyen).

Documentación ya recopilada en `LEGAL_TERCEROS` según el inventario de desarrollo: licencia de Ultralytics 8.4.157; archivos de licencia de PyTorch y torchvision; `LICENSE.txt` y `LICENSE-3RD-PARTY.txt` de OpenCV; licencia MIT-CMU de Pillow 12.3.0; licencia MIT de `pillow-avif-plugin` 1.6.0; `LICENSE.txt` y `LICENSES_bundled.txt` de `pi-heif` 1.4.0. Esto confirma **recopilación de documentos**, no revisión exhaustiva de todos los binarios o dependencias transitivas. La licencia de NumPy y la cobertura de todos los componentes redistribuidos requieren comprobación adicional.

**Pendiente:** completar la identificación de licencias, titulares de derechos y avisos de las versiones efectivamente incluidas, así como de sus dependencias transitivas. `requirements.txt` documenta el entorno de desarrollo, no prueba por sí solo el contenido del ejecutable.

## 5. Microsoft Visual C++ Runtime y otras bibliotecas nativas

Se identificó `VCOMP140.DLL` en la compilación de prueba y en la aplicación instalada; `vcomp140d.dll` (depuración) **no apareció** en esas dos ubicaciones. El registro `Analysis-00.toc` de PyInstaller indicó que `VCOMP140.DLL` se tomó de la carpeta raíz del proyecto. La versión previamente incluida era `14.31.31103.0`, firmada por Microsoft.

Se sustituyó **solo la copia del proyecto**, conservando un respaldo fuera de él, por la DLL de escritorio x64 procedente de la carpeta oficial de Visual Studio 2022 Build Tools:

`VC\Redist\MSVC\14.44.35112\x64\Microsoft.VC143.OpenMP\vcomp140.dll`

- Versión: **14.44.35211.0**; arquitectura: **x64**; firma Authenticode: **válida**, Microsoft Corporation.
- SHA-256 de la copia del proyecto y de la copia de `VC\Redist`: **idéntico**, `55ABA23CDCD6484FBB06F4155B8CA75ADFCE7A881F10AFD0C49457165E677164`.
- En una carpeta aislada, `realesrgan-ncnn-vulkan.exe` generó correctamente una imagen de salida utilizando esta versión de la DLL. Esto es una prueba funcional puntual, no una garantía universal de compatibilidad.
- **La instalación y el instalador existentes aún contienen la versión anterior** hasta una nueva compilación e instalación verificadas.

**Pendiente:** verificar los derechos y condiciones concretas de redistribución de Microsoft aplicables al desarrollador y a esta DLL; comprobar que la compilación final tome la nueva versión, que la aplicación siga funcionando y que no incluya DLL de depuración u otros archivos no autorizados. La firma válida y la ubicación `VC\Redist` no sustituyen la verificación de la licencia.

---

## Estado de publicación

Este inventario es **provisional**. Antes de distribuir una versión definitiva se debe verificar el contenido real del instalador, completar los textos de licencia y avisos aplicables, comprobar la disponibilidad del código fuente correspondiente y revisar por separado el cumplimiento de la distribución MSIX.

Los componentes de terceros conservan sus propias licencias y avisos de copyright. Este documento no constituye asesoramiento jurídico ni certificación de cumplimiento.
