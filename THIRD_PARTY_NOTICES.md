# Componentes de terceros — revisión pendiente

- **Ultralytics YOLO** (`ultralytics`, `yolo11n.pt`): consultar licencia AGPL-3.0 y términos de pesos de modelos; preparar el código fuente correspondiente y avisos. https://github.com/ultralytics/ultralytics
- **Real-ESRGAN NCNN Vulkan** (ejecutable y `models/*.bin`, `*.param`): comprobar licencias del proyecto, de los pesos y dependencias antes de redistribuir. https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan
- **PySide6 / Qt**: revisar LGPL/GPL y obligaciones de distribución (incluido reemplazo de bibliotecas). https://doc.qt.io/qtforpython-6/licenses.html
- **PyTorch, torchvision, OpenCV, Pillow, pillow-avif-plugin, NumPy, PyInstaller**: verificar avisos y licencias de las versiones efectivamente incluidas en el paquete.
- **Microsoft Visual C++ runtime DLLs**: verificar derechos de redistribución; no incluir bibliotecas de depuración en un lanzamiento público.

Este archivo es una lista de comprobación, **no una certificación de cumplimiento**.
