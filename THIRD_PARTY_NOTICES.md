
# Componentes de terceros — SmartCrop AI

Este documento identifica componentes externos utilizados por
SmartCrop AI y sus condiciones de licencia conocidas.

## 1. Ultralytics YOLO

Componentes: ultralytics y modelo yolo11n.pt.

Proyecto:
https://github.com/ultralytics/ultralytics

Licencia: GNU Affero General Public License v3.0
(AGPL-3.0), sujeta a los términos aplicables.

El código original de SmartCrop AI también se publica
bajo AGPL-3.0.

Pendiente: verificar los requisitos de distribución del
modelo y del código fuente correspondiente a la versión
incluida en la aplicación.

## 2. Real-ESRGAN NCNN Vulkan

Componente: realesrgan-ncnn-vulkan.exe.

Proyecto:
https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan

Distribución identificada:
realesrgan-ncnn-vulkan-20220424-windows

Licencia del proyecto: MIT.

Copyright original:
- Copyright (c) 2021 Xintao Wang
- Copyright (c) 2019 nihui

El ejecutable utilizado por SmartCrop AI fue comparado
con el archivo descargado de la distribución oficial.
Ambos archivos tienen el mismo hash SHA-256:

07E49F7CBB4EDE01AE4DD4C399D3A7E5846E3D2085C3128EFF881E55CB7B1A0C

Texto completo de la licencia:
[LICENSE-Real-ESRGAN.txt](LICENSE-Real-ESRGAN.txt)

Los 10 archivos de modelos (.bin y .param) incluidos
en SmartCrop AI fueron comparados mediante SHA-256
con los correspondientes archivos de la distribución
oficial realesrgan-ncnn-vulkan-20220424-windows.

Resultado: los 10 archivos son idénticos.

Modelos verificados:
- realesr-animevideov3-x2
- realesr-animevideov3-x3
- realesr-animevideov3-x4
- realesrgan-x4plus-anime
- realesrgan-x4plus

Pendiente: confirmar las licencias y condiciones
de redistribución específicas de los pesos de
los modelos.


También deben revisarse las dependencias binarias
incluidas en la distribución.

## 3. PySide6 / Qt

Proyecto:
https://doc.qt.io/qtforpython-6/licenses.html

PySide6 y los módulos Qt pueden estar sujetos a LGPL,
GPL u otras licencias según los componentes utilizados.

Pendiente: verificar los módulos efectivamente incluidos
y cumplir las obligaciones de distribución aplicables.

## 4. Bibliotecas de Python

Componentes utilizados:
- PyTorch y torchvision
- OpenCV
- Pillow
- pillow-avif-plugin
- NumPy
- PyInstaller

Pendiente: documentar las licencias y avisos de las
versiones efectivamente incluidas en el paquete.

El repositorio incluye un listado de las versiones
instaladas en el entorno de desarrollo.

## 5. Microsoft Visual C++ Runtime

Pendiente: verificar las condiciones de redistribución
de las bibliotecas incluidas en el instalador.

No deben distribuirse bibliotecas de depuración que
no estén autorizadas para redistribución.

---

Este documento se encuentra en revisión y no constituye
una certificación de cumplimiento de licencias.

Los componentes de terceros conservan sus respectivas
licencias y avisos de copyright.
