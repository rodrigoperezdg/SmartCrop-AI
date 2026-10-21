import sys
import os
import subprocess
import winsound
import time

try:
    import pillow_avif  # Registra soporte AVIF en Pillow (requiere pillow-avif-plugin)
    AVIF_DISPONIBLE = True
except ImportError:
    AVIF_DISPONIBLE = False

from PIL import Image
import cv2
from ultralytics import YOLO

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QScrollArea,
    QGridLayout,
    QComboBox,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QProgressDialog,
    QCheckBox,
    QSlider,
    QLineEdit,
    QGroupBox
)

from PySide6.QtGui import (
    QPixmap,
    QImage
)

from PySide6.QtCore import (
    Qt,
    QPoint,
    QTimer
)


# ============================================================
# APLICACIÓN
# ============================================================

app = QApplication(sys.argv)

ventana = QWidget()

ventana.setWindowTitle(
    "SmartCrop AI"
)

ventana.resize(
    1200,
    800
)


# ============================================================
# REAL-ESRGAN / RECURSOS
# ============================================================

if getattr(sys, "frozen", False):

    CARPETA_APP = os.path.dirname(
        os.path.abspath(
            sys.executable
        )
    )

    CARPETA_RECURSOS = os.path.join(
        CARPETA_APP,
        "_internal"
    )

else:

    CARPETA_APP = os.path.dirname(
        os.path.abspath(__file__)
    )

    CARPETA_RECURSOS = CARPETA_APP


# ------------------------------------------------------------
# Real-ESRGAN
# ------------------------------------------------------------

RUTA_ESRGAN = os.path.join(
    CARPETA_RECURSOS,
    "realesrgan-ncnn-vulkan.exe"
)

CARPETA_MODELOS = os.path.join(
    CARPETA_RECURSOS,
    "models"
)


# ------------------------------------------------------------
# Fallback:
# por si Real-ESRGAN está al lado del EXE
# ------------------------------------------------------------

if not os.path.isfile(
    RUTA_ESRGAN
):

    ruta_alternativa = os.path.join(
        CARPETA_APP,
        "realesrgan-ncnn-vulkan.exe"
    )

    modelos_alternativos = os.path.join(
        CARPETA_APP,
        "models"
    )

    if os.path.isfile(
        ruta_alternativa
    ):

        RUTA_ESRGAN = (
            ruta_alternativa
        )

        CARPETA_MODELOS = (
            modelos_alternativos
        )


def es_real_esrgan_disponible():

    return (
        os.path.isfile(
            RUTA_ESRGAN
        )
        and
        os.path.isdir(
            CARPETA_MODELOS
        )
    )


# ============================================================
# MODELO YOLO
# ============================================================

print(
    "Cargando modelo YOLO..."
)

ruta_yolo = os.path.join(
    CARPETA_RECURSOS,
    "yolo11n.pt"
)

# Fallback para desarrollo o builds
# donde el modelo quede al lado del EXE.

if not os.path.isfile(
    ruta_yolo
):

    ruta_yolo_alternativa = os.path.join(
        CARPETA_APP,
        "yolo11n.pt"
    )

    if os.path.isfile(
        ruta_yolo_alternativa
    ):

        ruta_yolo = (
            ruta_yolo_alternativa
        )


modelo_yolo = YOLO(
    ruta_yolo
)

print(
    "Modelo YOLO cargado."
)


detector_caras = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ============================================================
# VARIABLES
# ============================================================

archivos_seleccionados = []

analisis_cache = {}

# Seguimiento opcional de carpeta
carpeta_monitoreada = ""
archivos_vistos_carpeta = set()
archivos_pendientes_estabilidad = {}

ajustes_manuales = {}

fotos_mejorar_ia = {}

prefijos_salida = {}

sufijos_salida = {}

tamano_miniatura = 520


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

layout_principal = QVBoxLayout(
    ventana
)


titulo = QLabel(
    "SmartCrop AI"
)

titulo.setAlignment(
    Qt.AlignCenter
)

titulo.setStyleSheet("""
    QLabel {
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
    }
""")

layout_principal.addWidget(
    titulo
)


# ============================================================
# CONTROLES PRINCIPALES
# ============================================================

layout_controles = QHBoxLayout()


# ------------------------------------------------------------
# SELECCIONAR
# ------------------------------------------------------------

boton_seleccionar = QPushButton(
    "Seleccionar fotos"
)

boton_seleccionar.setMinimumHeight(
    40
)

layout_controles.addWidget(
    boton_seleccionar
)


# ------------------------------------------------------------
# CARPETA SINCRONIZADA
# ------------------------------------------------------------

boton_carpeta = QPushButton("Vigilar carpeta…")
boton_carpeta.setMinimumHeight(40)
layout_controles.addWidget(boton_carpeta)

boton_detener_carpeta = QPushButton("Detener vigilancia")
boton_detener_carpeta.setMinimumHeight(40)
boton_detener_carpeta.setEnabled(False)
layout_controles.addWidget(boton_detener_carpeta)

boton_limpiar = QPushButton("Limpiar todo")
boton_limpiar.setMinimumHeight(40)
layout_controles.addWidget(boton_limpiar)


# ------------------------------------------------------------
# FORMATO
# ------------------------------------------------------------

formato = QComboBox()

formato.setMinimumHeight(
    40
)

formato.addItem(
    "1920 × 880",
    (1920, 880)
)

formato.addItem(
    "1920 × 1080",
    (1920, 1080)
)

formato.addItem(
    "1080 × 1350",
    (1080, 1350)
)

formato.addItem(
    "1080 × 1920",
    (1080, 1920)
)

layout_controles.addWidget(
    formato
)


# ------------------------------------------------------------
# FORMATO DE ARCHIVO
# ------------------------------------------------------------

formato_salida = QComboBox()

formato_salida.setMinimumHeight(
    40
)

formato_salida.addItem(
    "JPG",
    "jpg"
)

formato_salida.addItem(
    "PNG",
    "png"
)

layout_controles.addWidget(
    formato_salida
)


# ------------------------------------------------------------
# REAL-ESRGAN
# ------------------------------------------------------------

mejora_ia = QComboBox()

mejora_ia.setMinimumHeight(
    40
)

mejora_ia.addItem(
    "IA: Desactivada",
    0
)

mejora_ia.addItem(
    "IA: Real-ESRGAN",
    4
)

layout_controles.addWidget(
    mejora_ia
)


# ------------------------------------------------------------
# IA TODAS
# ------------------------------------------------------------

boton_ia_todas = QPushButton(
    "✨ IA: Seleccionar todas"
)

boton_ia_todas.setMinimumHeight(
    40
)

layout_controles.addWidget(
    boton_ia_todas
)


# ------------------------------------------------------------
# EXPORTAR
# ------------------------------------------------------------

boton_exportar = QPushButton(
    "EXPORTAR"
)

boton_exportar.setMinimumHeight(
    40
)

boton_exportar.setMinimumWidth(
    150
)

boton_exportar.setStyleSheet("""
    QPushButton {
        background-color: #22a447;
        color: white;
        font-size: 15px;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 8px 18px;
    }

    QPushButton:hover {
        background-color: #1d8f3d;
    }

    QPushButton:pressed {
        background-color: #176f30;
    }

    QPushButton:disabled {
        background-color: #777777;
        color: #dddddd;
    }
""")

layout_controles.addWidget(
    boton_exportar
)


layout_principal.addLayout(
    layout_controles
)


# ============================================================
# NOMBRES DE SALIDA
# ============================================================

grupo_nombres = QGroupBox(
    "Nombre de salida"
)

layout_nombres = QHBoxLayout(
    grupo_nombres
)


label_prefijo = QLabel(
    "Prefijo:"
)

layout_nombres.addWidget(
    label_prefijo
)


prefijo_global = QLineEdit()

prefijo_global.setPlaceholderText(
    "Ej: MUNDIAL_"
)

prefijo_global.setMinimumHeight(
    32
)

layout_nombres.addWidget(
    prefijo_global
)


label_sufijo = QLabel(
    "Sufijo:"
)

layout_nombres.addWidget(
    label_sufijo
)


sufijo_global = QLineEdit()

sufijo_global.setPlaceholderText(
    "Ej: _FINAL"
)

sufijo_global.setMinimumHeight(
    32
)

layout_nombres.addWidget(
    sufijo_global
)


boton_aplicar_nombres = QPushButton(
    "Aplicar a todas"
)

boton_aplicar_nombres.setMinimumHeight(
    32
)

layout_nombres.addWidget(
    boton_aplicar_nombres
)


layout_principal.addWidget(
    grupo_nombres
)


# ============================================================
# TAMAÑO DE MINIATURAS
# ============================================================

fila_miniaturas = QHBoxLayout()


label_miniaturas = QLabel(
    "Tamaño de miniaturas:"
)

fila_miniaturas.addWidget(
    label_miniaturas
)


boton_menos = QPushButton(
    "−"
)

boton_menos.setFixedWidth(
    35
)

fila_miniaturas.addWidget(
    boton_menos
)


slider_miniaturas = QSlider(
    Qt.Horizontal
)

slider_miniaturas.setMinimum(
    250
)

slider_miniaturas.setMaximum(
    700
)

slider_miniaturas.setValue(
    tamano_miniatura
)

slider_miniaturas.setSingleStep(
    25
)

slider_miniaturas.setPageStep(
    50
)

fila_miniaturas.addWidget(
    slider_miniaturas
)


boton_mas = QPushButton(
    "+"
)

boton_mas.setFixedWidth(
    35
)

fila_miniaturas.addWidget(
    boton_mas
)


label_tamano_miniaturas = QLabel(
    f"{tamano_miniatura}px"
)

label_tamano_miniaturas.setMinimumWidth(
    60
)

fila_miniaturas.addWidget(
    label_tamano_miniaturas
)


layout_principal.addLayout(
    fila_miniaturas
)


# ============================================================
# ÁREA DE FOTOS
# ============================================================

scroll = QScrollArea()

scroll.setWidgetResizable(
    True
)

contenedor = QWidget()

grid = QGridLayout(
    contenedor
)

grid.setSpacing(
    20
)

scroll.setWidget(
    contenedor
)

layout_principal.addWidget(
    scroll
)


# ============================================================
# PILLOW → QPIXMAP
# ============================================================

def pillow_a_pixmap(
    imagen
):

    imagen = imagen.convert(
        "RGB"
    )

    datos = imagen.tobytes(
        "raw",
        "RGB"
    )

    qimage = QImage(
        datos,
        imagen.width,
        imagen.height,
        imagen.width * 3,
        QImage.Format_RGB888
    )

    return QPixmap.fromImage(
        qimage.copy()
    )


# ============================================================
# ANALIZAR RESOLUCIÓN
# ============================================================

def obtener_estado_resolucion(
    archivo,
    ancho_salida,
    alto_salida
):

    try:

        with Image.open(
            archivo
        ) as imagen:

            ancho_original = imagen.width
            alto_original = imagen.height

    except Exception:

        return {
            "estado": "verde",
            "icono": "🟢",
            "titulo": "Resolución no disponible",
            "tooltip": (
                "No se pudo determinar "
                "la resolución original."
            ),
            "ancho_original": 0,
            "alto_original": 0
        }


    porcentaje_ancho = (
        ancho_original /
        ancho_salida
        if ancho_salida > 0
        else 1
    )


    porcentaje_alto = (
        alto_original /
        alto_salida
        if alto_salida > 0
        else 1
    )


    porcentaje_minimo = min(
        porcentaje_ancho,
        porcentaje_alto
    )


    if (
        ancho_original >= ancho_salida
        and
        alto_original >= alto_salida
    ):

        estado = "verde"

        icono = "🟢"

        titulo = (
            "Resolución suficiente"
        )

        recomendacion = (
            "No necesita escalado por resolución."
        )


    elif porcentaje_minimo < 0.80:

        estado = "rojo"

        icono = "🔴"

        titulo = (
            "Resolución baja"
        )

        recomendacion = (
            "Se recomienda considerar "
            "Real-ESRGAN."
        )


    else:

        estado = "amarillo"

        icono = "🟡"

        titulo = (
            "Resolución justa"
        )

        recomendacion = (
            "La imagen puede exportarse, "
            "pero puede beneficiarse de "
            "Real-ESRGAN."
        )


    tooltip = (
        f"{icono} {titulo}\n\n"
        f"Original: "
        f"{ancho_original} × {alto_original}\n"
        f"Salida: "
        f"{ancho_salida} × {alto_salida}\n\n"
        f"{recomendacion}"
    )


    return {
        "estado": estado,
        "icono": icono,
        "titulo": titulo,
        "tooltip": tooltip,
        "ancho_original": ancho_original,
        "alto_original": alto_original,
        "porcentaje_ancho": porcentaje_ancho,
        "porcentaje_alto": porcentaje_alto,
        "porcentaje_minimo": porcentaje_minimo
    }


# ============================================================
# COMPROBAR RESOLUCIÓN
# ============================================================

def imagen_es_mas_chica_que_formato(
    archivo,
    ancho_salida,
    alto_salida
):

    estado = obtener_estado_resolucion(
        archivo,
        ancho_salida,
        alto_salida
    )

    return (
        estado["estado"] != "verde"
    )


# ============================================================
# ANÁLISIS IA
# ============================================================

def analizar_foto(
    archivo
):

    if archivo in analisis_cache:

        return analisis_cache[
            archivo
        ]


    print()
    print(
        "Analizando con IA:"
    )

    print(
        archivo
    )


    try:
        imagen_pil = Image.open(archivo).convert("RGB")
        import numpy as np
        imagen_cv = cv2.cvtColor(
            np.array(imagen_pil),
            cv2.COLOR_RGB2BGR
        )
    except Exception:
        imagen_cv = None

    caras = []


    # --------------------------------------------------------
    # CARAS
    # --------------------------------------------------------

    if imagen_cv is not None:

        gris = cv2.cvtColor(
            imagen_cv,
            cv2.COLOR_BGR2GRAY
        )

        detecciones_caras = (
            detector_caras.detectMultiScale(
                gris,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50)
            )
        )

        for x, y, ancho, alto in (
            detecciones_caras
        ):

            caras.append({
                "bbox": (
                    x,
                    y,
                    x + ancho,
                    y + alto
                ),
                "centro": (
                    x + ancho // 2,
                    y + alto // 2
                )
            })


    # --------------------------------------------------------
    # YOLO
    # --------------------------------------------------------

    resultados = modelo_yolo(
        archivo,
        verbose=False
    )

    objetos = []


    for resultado in resultados:

        if resultado.boxes is None:

            continue


        for box in resultado.boxes:

            x1, y1, x2, y2 = (
                box.xyxy[0]
                .cpu()
                .numpy()
            )

            confianza = float(
                box.conf[0]
                .cpu()
                .numpy()
            )

            clase = int(
                box.cls[0]
                .cpu()
                .numpy()
            )

            nombre = (
                modelo_yolo.names[
                    clase
                ]
            )


            objetos.append({
                "nombre": nombre,
                "confianza": confianza,
                "bbox": (
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ),
                "centro": (
                    int(
                        (x1 + x2) / 2
                    ),
                    int(
                        (y1 + y2) / 2
                    )
                )
            })


    # --------------------------------------------------------
    # PERSONAS
    # --------------------------------------------------------

    personas = [
        o
        for o in objetos
        if (
            o["nombre"] == "person"
            and
            o["confianza"] >= 0.40
        )
    ]


    grupo = None


    # --------------------------------------------------------
    # GRUPO
    # --------------------------------------------------------

    if personas:

        x1 = min(
            p["bbox"][0]
            for p in personas
        )

        y1 = min(
            p["bbox"][1]
            for p in personas
        )

        x2 = max(
            p["bbox"][2]
            for p in personas
        )

        y2 = max(
            p["bbox"][3]
            for p in personas
        )


        ancho = max(
            1,
            x2 - x1
        )

        alto = max(
            1,
            y2 - y1
        )


        margen_x = max(
            20,
            int(
                ancho * 0.08
            )
        )


        margen_arriba = max(
            35,
            int(
                alto * 0.18
            )
        )


        margen_abajo = max(
            20,
            int(
                alto * 0.08
            )
        )


        grupo = (
            x1 - margen_x,
            y1 - margen_arriba,
            x2 + margen_x,
            y2 + margen_abajo
        )


    # --------------------------------------------------------
    # PUNTO DE INTERÉS
    # --------------------------------------------------------

    punto = None


    if personas:

        promedio_x = int(
            sum(
                p["centro"][0]
                for p in personas
            )
            /
            len(personas)
        )


        promedio_y = int(
            sum(
                p["centro"][1]
                for p in personas
            )
            /
            len(personas)
        )


        if caras:

            promedio_cara_y = int(
                sum(
                    c["centro"][1]
                    for c in caras
                )
                /
                len(caras)
            )


            promedio_y = int(
                (
                    promedio_y
                    +
                    promedio_cara_y * 2
                )
                /
                3
            )


        punto = (
            promedio_x,
            promedio_y
        )


    else:

        objetos_validos = [
            o
            for o in objetos
            if o["confianza"] >= 0.45
        ]


        if objetos_validos:

            principal = max(
                objetos_validos,
                key=lambda x:
                x["confianza"]
            )

            punto = principal[
                "centro"
            ]


        elif caras:

            punto = (
                int(
                    sum(
                        c["centro"][0]
                        for c in caras
                    )
                    /
                    len(caras)
                ),
                int(
                    sum(
                        c["centro"][1]
                        for c in caras
                    )
                    /
                    len(caras)
                )
            )


    analisis = {
        "personas": personas,
        "caras": caras,
        "objetos": objetos,
        "grupo": grupo,
        "punto": punto
    }


    analisis_cache[
        archivo
    ] = analisis


    print(
        "  Personas:",
        len(personas)
    )

    print(
        "  Caras:",
        len(caras)
    )


    return analisis


# ============================================================
# CROP DE GRUPO
# ============================================================

def calcular_crop_grupo(
    ancho_original,
    alto_original,
    ancho_salida,
    alto_salida,
    grupo
):

    x1, y1, x2, y2 = grupo


    x1 = max(
        0,
        x1
    )

    y1 = max(
        0,
        y1
    )

    x2 = min(
        ancho_original,
        x2
    )

    y2 = min(
        alto_original,
        y2
    )


    ancho_grupo = max(
        1,
        x2 - x1
    )

    alto_grupo = max(
        1,
        y2 - y1
    )


    ratio = (
        ancho_salida /
        alto_salida
    )


    ratio_grupo = (
        ancho_grupo /
        alto_grupo
    )


    if ratio_grupo > ratio:

        crop_ancho = ancho_grupo

        crop_alto = int(
            crop_ancho /
            ratio
        )

    else:

        crop_alto = alto_grupo

        crop_ancho = int(
            crop_alto *
            ratio
        )


    if crop_ancho > ancho_original:

        crop_ancho = (
            ancho_original
        )

        crop_alto = int(
            crop_ancho /
            ratio
        )


    if crop_alto > alto_original:

        crop_alto = (
            alto_original
        )

        crop_ancho = int(
            crop_alto *
            ratio
        )


    centro_x = (
        x1 + x2
    ) / 2

    centro_y = (
        y1 + y2
    ) / 2


    izquierda = int(
        centro_x -
        crop_ancho / 2
    )

    arriba = int(
        centro_y -
        crop_alto / 2
    )


    izquierda = max(
        0,
        min(
            izquierda,
            ancho_original -
            crop_ancho
        )
    )


    arriba = max(
        0,
        min(
            arriba,
            alto_original -
            crop_alto
        )
    )


    return (
        izquierda,
        arriba,
        izquierda +
        crop_ancho,
        arriba +
        crop_alto
    )


# ============================================================
# CROP NORMAL
# ============================================================

def calcular_crop_normal(
    imagen,
    ancho_salida,
    alto_salida,
    centro=None
):

    ancho_original = (
        imagen.width
    )

    alto_original = (
        imagen.height
    )


    ratio_original = (
        ancho_original /
        alto_original
    )

    ratio_salida = (
        ancho_salida /
        alto_salida
    )


    if ratio_original > ratio_salida:

        crop_ancho = int(
            alto_original *
            ratio_salida
        )


        if centro:

            izquierda = int(
                centro[0]
                -
                crop_ancho / 2
            )

        else:

            izquierda = int(
                (
                    ancho_original -
                    crop_ancho
                ) / 2
            )


        izquierda = max(
            0,
            min(
                izquierda,
                ancho_original -
                crop_ancho
            )
        )


        arriba = 0

        derecha = (
            izquierda +
            crop_ancho
        )

        abajo = (
            alto_original
        )


    else:

        crop_alto = int(
            ancho_original /
            ratio_salida
        )


        if centro:

            arriba = int(
                centro[1]
                -
                crop_alto / 2
            )

        else:

            arriba = int(
                (
                    alto_original -
                    crop_alto
                ) / 2
            )


        arriba = max(
            0,
            min(
                arriba,
                alto_original -
                crop_alto
            )
        )


        izquierda = 0

        derecha = (
            ancho_original
        )

        abajo = (
            arriba +
            crop_alto
        )


    return (
        izquierda,
        arriba,
        derecha,
        abajo
    )


# ============================================================
# CROP AUTOMÁTICO
# ============================================================

def obtener_crop_automatico(
    archivo,
    imagen,
    ancho_salida,
    alto_salida
):

    analisis = analizar_foto(
        archivo
    )


    grupo = analisis[
        "grupo"
    ]


    if grupo:

        return calcular_crop_grupo(
            imagen.width,
            imagen.height,
            ancho_salida,
            alto_salida,
            grupo
        )


    return calcular_crop_normal(
        imagen,
        ancho_salida,
        alto_salida,
        analisis["punto"]
    )


# ============================================================
# CROP ACTUAL
# ============================================================

def obtener_crop_actual(
    archivo,
    imagen,
    ancho_salida,
    alto_salida
):

    crop_automatico = (
        obtener_crop_automatico(
            archivo,
            imagen,
            ancho_salida,
            alto_salida
        )
    )


    ajustes = ajustes_manuales.get(
        archivo
    )


    if not ajustes:

        return crop_automatico


    x1, y1, x2, y2 = (
        crop_automatico
    )


    ancho_crop = (
        x2 - x1
    )

    alto_crop = (
        y2 - y1
    )


    zoom = ajustes[
        "zoom"
    ]


    nuevo_ancho = int(
        ancho_crop /
        zoom
    )

    nuevo_alto = int(
        alto_crop /
        zoom
    )


    nuevo_ancho = max(
        10,
        min(
            nuevo_ancho,
            imagen.width
        )
    )

    nuevo_alto = max(
        10,
        min(
            nuevo_alto,
            imagen.height
        )
    )


    centro_x = (
        x1 + x2
    ) / 2

    centro_y = (
        y1 + y2
    ) / 2


    centro_x += (
        ajustes["x"] *
        imagen.width
    )

    centro_y += (
        ajustes["y"] *
        imagen.height
    )


    izquierda = int(
        centro_x -
        nuevo_ancho / 2
    )

    arriba = int(
        centro_y -
        nuevo_alto / 2
    )


    izquierda = max(
        0,
        min(
            izquierda,
            imagen.width -
            nuevo_ancho
        )
    )


    arriba = max(
        0,
        min(
            arriba,
            imagen.height -
            nuevo_alto
        )
    )


    return (
        izquierda,
        arriba,
        izquierda +
        nuevo_ancho,
        arriba +
        nuevo_alto
    )


# ============================================================
# PREVIEW
# ============================================================

def generar_preview(
    archivo,
    ancho_salida,
    alto_salida
):

    imagen = Image.open(
        archivo
    ).convert(
        "RGB"
    )


    crop = obtener_crop_actual(
        archivo,
        imagen,
        ancho_salida,
        alto_salida
    )


    resultado = imagen.crop(
        crop
    )


    resultado = resultado.resize(
        (
            ancho_salida,
            alto_salida
        ),
        Image.Resampling.LANCZOS
    )


    return resultado


# ============================================================
# REAL-ESRGAN
# ============================================================

def mejorar_con_esrgan(
    imagen,
    escala,
    carpeta_temporal
):

    if escala == 0:

        return imagen


    if not es_real_esrgan_disponible():

        raise RuntimeError(
            "No se encontró Real-ESRGAN.\n\n"
            f"Ruta buscada:\n"
            f"{RUTA_ESRGAN}\n\n"
            f"Modelos buscados en:\n"
            f"{CARPETA_MODELOS}"
        )


    entrada = os.path.join(
        carpeta_temporal,
        "smartcrop_esrgan_input.png"
    )


    salida = os.path.join(
        carpeta_temporal,
        "smartcrop_esrgan_output.png"
    )


    imagen.save(
        entrada,
        "PNG"
    )


    comando = [
        RUTA_ESRGAN,

        "-i",
        entrada,

        "-o",
        salida,

        "-n",
        "realesrgan-x4plus",

        # El modelo realesrgan-x4plus trabaja de forma estable a su escala
        # nativa 4×. SmartCrop hace luego el resize final con LANCZOS.
        "-s",
        "4",

        "-t",
        "256",

        "-f",
        "png"
    ]


    print()
    print(
        "Ejecutando Real-ESRGAN:"
    )

    print(
        " ".join(comando)
    )

    print(
        "Ejecutable:",
        RUTA_ESRGAN
    )

    print(
        "Modelos:",
        CARPETA_MODELOS
    )


    opciones_subprocess = {}

    if sys.platform == "win32":

        opciones_subprocess["creationflags"] = (
            subprocess.CREATE_NO_WINDOW
        )


    resultado = subprocess.run(
        comando,
        cwd=os.path.dirname(
            RUTA_ESRGAN
        ),
        capture_output=True,
        text=True,
        **opciones_subprocess
    )


    if resultado.returncode != 0:

        print(
            resultado.stdout
        )

        print(
            resultado.stderr
        )

        raise RuntimeError(
            "Real-ESRGAN terminó con un error.\n\n"
            +
            resultado.stderr[-1500:]
        )


    if not os.path.isfile(
        salida
    ):

        raise RuntimeError(
            "Real-ESRGAN no generó "
            "el archivo de salida."
        )


    resultado_imagen = (
        Image.open(
            salida
        ).convert(
            "RGB"
        )
    )


    try:

        os.remove(
            entrada
        )

        os.remove(
            salida
        )

    except:

        pass


    return resultado_imagen


# ============================================================
# PROCESAR EXPORTACIÓN
# ============================================================

def procesar_exportacion(
    archivo,
    ancho,
    alto,
    escala_esrgan,
    carpeta_destino,
    extension_salida
):

    imagen = Image.open(
        archivo
    ).convert(
        "RGB"
    )


    crop = obtener_crop_actual(
        archivo,
        imagen,
        ancho,
        alto
    )


    resultado = imagen.crop(
        crop
    )


    # --------------------------------------------------------
    # IA
    # --------------------------------------------------------

    if escala_esrgan > 0:

        resultado = (
            mejorar_con_esrgan(
                resultado,
                escala_esrgan,
                carpeta_destino
            )
        )


    # --------------------------------------------------------
    # Resize final
    # --------------------------------------------------------

    resultado = resultado.resize(
        (
            ancho,
            alto
        ),
        Image.Resampling.LANCZOS
    )


    # --------------------------------------------------------
    # NOMBRE
    # --------------------------------------------------------

    nombre = os.path.splitext(
        os.path.basename(
            archivo
        )
    )[0]


    prefijo = prefijos_salida.get(
        archivo,
        ""
    )


    sufijo = sufijos_salida.get(
        archivo,
        ""
    )


    sufijo_automatico = "_smartcrop"


    if escala_esrgan > 0:

        sufijo_automatico += "_AI"


    nombre_final = (
        prefijo
        +
        nombre
        +
        sufijo
        +
        sufijo_automatico
    )


    salida = os.path.join(
        carpeta_destino,
        nombre_final +
        "." +
        extension_salida
    )


    # --------------------------------------------------------
    # GUARDAR JPG
    # --------------------------------------------------------

    if extension_salida == "jpg":

        resultado.save(
            salida,
            "JPEG",
            quality=95,
            subsampling=0
        )


    # --------------------------------------------------------
    # GUARDAR PNG
    # --------------------------------------------------------

    else:

        resultado.save(
            salida,
            "PNG",
            compress_level=6
        )


    return salida


# ============================================================
# EDITOR GRANDE
# ============================================================

class EditorGrande(QDialog):

    def __init__(
        self,
        archivo,
        ancho_salida,
        alto_salida,
        padre=None
    ):

        super().__init__(
            padre
        )


        self.archivo = archivo

        self.ancho_salida = (
            ancho_salida
        )

        self.alto_salida = (
            alto_salida
        )


        self.setWindowTitle(
            "SmartCrop AI — Editor"
        )

        self.resize(
            1200,
            800
        )


        self.imagen = Image.open(
            archivo
        ).convert(
            "RGB"
        )


        obtener_crop_automatico(
            archivo,
            self.imagen,
            ancho_salida,
            alto_salida
        )


        ajustes = ajustes_manuales.get(
            archivo,
            {
                "x": 0,
                "y": 0,
                "zoom": 1.0
            }
        )


        self.offset_x = (
            ajustes["x"]
        )

        self.offset_y = (
            ajustes["y"]
        )

        self.zoom = (
            ajustes["zoom"]
        )


        self.arrastrando = False

        self.ultimo_mouse = QPoint()


        self.crear_interfaz()

        self.actualizar()


    def crear_interfaz(
        self
    ):

        layout = QVBoxLayout(
            self
        )


        self.preview = QLabel()

        self.preview.setAlignment(
            Qt.AlignCenter
        )

        self.preview.setMinimumSize(
            800,
            550
        )

        self.preview.setStyleSheet("""
            QLabel {
                background: #111111;
            }
        """)


        self.preview.mousePressEvent = (
            self.mouse_press
        )

        self.preview.mouseMoveEvent = (
            self.mouse_move
        )

        self.preview.mouseReleaseEvent = (
            self.mouse_release
        )

        self.preview.wheelEvent = (
            self.mouse_wheel
        )


        layout.addWidget(
            self.preview
        )


        instrucciones = QLabel(
            "🖐 Arrastrá para mover  •  "
            "🔍 Rueda para zoom"
        )


        instrucciones.setAlignment(
            Qt.AlignCenter
        )


        layout.addWidget(
            instrucciones
        )


        botones = QHBoxLayout()


        boton_auto = QPushButton(
            "↺ Automático"
        )

        boton_auto.setMinimumHeight(
            40
        )

        boton_auto.clicked.connect(
            self.restaurar_automatico
        )

        botones.addWidget(
            boton_auto
        )


        boton_listo = QPushButton(
            "✓ LISTO"
        )

        boton_listo.setMinimumHeight(
            40
        )

        boton_listo.clicked.connect(
            self.accept
        )

        botones.addWidget(
            boton_listo
        )


        layout.addLayout(
            botones
        )


    def mouse_press(
        self,
        evento
    ):

        if evento.button() != (
            Qt.LeftButton
        ):

            return


        self.arrastrando = True

        self.ultimo_mouse = (
            evento.position()
            .toPoint()
        )


        self.preview.setCursor(
            Qt.ClosedHandCursor
        )


    def mouse_move(
        self,
        evento
    ):

        if not self.arrastrando:

            return


        actual = (
            evento.position()
            .toPoint()
        )


        delta = (
            actual -
            self.ultimo_mouse
        )


        ancho_preview = max(
            1,
            self.preview.width()
        )

        alto_preview = max(
            1,
            self.preview.height()
        )


        self.offset_x -= (
            delta.x() /
            ancho_preview
        )

        self.offset_y -= (
            delta.y() /
            alto_preview
        )


        self.offset_x = max(
            -0.5,
            min(
                0.5,
                self.offset_x
            )
        )

        self.offset_y = max(
            -0.5,
            min(
                0.5,
                self.offset_y
            )
        )


        self.ultimo_mouse = actual

        self.guardar_ajustes()

        self.actualizar()


    def mouse_release(
        self,
        evento
    ):

        if evento.button() != (
            Qt.LeftButton
        ):

            return


        self.arrastrando = False

        self.preview.setCursor(
            Qt.OpenHandCursor
        )


    def mouse_wheel(
        self,
        evento
    ):

        delta = (
            evento.angleDelta().y()
        )


        if delta > 0:

            self.zoom *= 1.08

        else:

            self.zoom /= 1.08


        self.zoom = max(
            1.0,
            min(
                3.0,
                self.zoom
            )
        )


        self.guardar_ajustes()

        self.actualizar()


    def guardar_ajustes(
        self
    ):

        ajustes_manuales[
            self.archivo
        ] = {
            "x": self.offset_x,
            "y": self.offset_y,
            "zoom": self.zoom
        }


    def restaurar_automatico(
        self
    ):

        self.offset_x = 0

        self.offset_y = 0

        self.zoom = 1.0


        if self.archivo in (
            ajustes_manuales
        ):

            del ajustes_manuales[
                self.archivo
            ]


        self.actualizar()


    def actualizar(
        self
    ):

        crop = obtener_crop_actual(
            self.archivo,
            self.imagen,
            self.ancho_salida,
            self.alto_salida
        )


        resultado = self.imagen.crop(
            crop
        )


        resultado = resultado.resize(
            (
                self.ancho_salida,
                self.alto_salida
            ),
            Image.Resampling.LANCZOS
        )


        pixmap = pillow_a_pixmap(
            resultado
        )


        pixmap = pixmap.scaled(
            self.preview.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.preview.setPixmap(
            pixmap
        )


        self.preview.setCursor(
            Qt.OpenHandCursor
        )


# ============================================================
# PREVIEW INTERACTIVO
# ============================================================

class PreviewInteractivo(
    QLabel
):

    def __init__(
        self,
        tarjeta
    ):

        super().__init__()

        self.tarjeta = tarjeta

        self.arrastrando = False

        self.ultimo_mouse = QPoint()


        self.setAlignment(
            Qt.AlignCenter
        )

        self.setMouseTracking(
            True
        )

        self.setCursor(
            Qt.OpenHandCursor
        )


        self.setStyleSheet("""
            QLabel {
                background: #202020;
                border-radius: 6px;
            }

            QLabel:hover {
                background: #181818;
            }
        """)


    def mousePressEvent(
        self,
        evento
    ):

        if evento.button() != (
            Qt.LeftButton
        ):

            return


        self.arrastrando = True

        self.ultimo_mouse = (
            evento.position()
            .toPoint()
        )


        self.setCursor(
            Qt.ClosedHandCursor
        )


    def mouseMoveEvent(
        self,
        evento
    ):

        if not self.arrastrando:

            return


        actual = (
            evento.position()
            .toPoint()
        )


        delta = (
            actual -
            self.ultimo_mouse
        )


        ancho = max(
            1,
            self.width()
        )

        alto = max(
            1,
            self.height()
        )


        self.tarjeta.offset_x -= (
            delta.x() /
            ancho
        )

        self.tarjeta.offset_y -= (
            delta.y() /
            alto
        )


        self.tarjeta.offset_x = max(
            -0.5,
            min(
                0.5,
                self.tarjeta.offset_x
            )
        )


        self.tarjeta.offset_y = max(
            -0.5,
            min(
                0.5,
                self.tarjeta.offset_y
            )
        )


        self.tarjeta.guardar_ajustes()

        self.ultimo_mouse = actual

        self.tarjeta.actualizar_preview()


    def mouseReleaseEvent(
        self,
        evento
    ):

        if evento.button() != (
            Qt.LeftButton
        ):

            return


        self.arrastrando = False

        self.setCursor(
            Qt.OpenHandCursor
        )


    def wheelEvent(
        self,
        evento
    ):

        delta = (
            evento.angleDelta().y()
        )


        if delta > 0:

            self.tarjeta.zoom *= 1.08

        else:

            self.tarjeta.zoom /= 1.08


        self.tarjeta.zoom = max(
            1.0,
            min(
                3.0,
                self.tarjeta.zoom
            )
        )


        self.tarjeta.guardar_ajustes()

        self.tarjeta.actualizar_preview()


        evento.accept()


    def mouseDoubleClickEvent(
        self,
        evento
    ):

        if evento.button() != (
            Qt.LeftButton
        ):

            return


        self.tarjeta.abrir_editor()

        evento.accept()


# ============================================================
# TARJETA DE FOTO
# ============================================================

class FotoEditor(
    QWidget
):

    def __init__(
        self,
        archivo,
        ancho,
        alto,
        padre=None
    ):

        super().__init__(
            padre
        )


        self.archivo = archivo

        self.ancho = ancho

        self.alto = alto


        ajustes = ajustes_manuales.get(
            archivo,
            {
                "x": 0,
                "y": 0,
                "zoom": 1.0
            }
        )


        self.offset_x = (
            ajustes["x"]
        )

        self.offset_y = (
            ajustes["y"]
        )

        self.zoom = (
            ajustes["zoom"]
        )


        self.crear_interfaz()

        self.actualizar_preview()


    def crear_interfaz(
        self
    ):

        layout = QVBoxLayout(
            self
        )


        # ----------------------------------------------------
        # PREVIEW
        # ----------------------------------------------------

        self.preview = (
            PreviewInteractivo(
                self
            )
        )


        layout.addWidget(
            self.preview
        )


        # ----------------------------------------------------
        # NOMBRE + RESOLUCIÓN
        # ----------------------------------------------------

        fila_info = QHBoxLayout()


        nombre = QLabel(
            os.path.basename(
                self.archivo
            )
        )


        nombre.setAlignment(
            Qt.AlignCenter
        )

        nombre.setWordWrap(
            True
        )


        fila_info.addWidget(
            nombre,
            1
        )


        estado_resolucion = (
            obtener_estado_resolucion(
                self.archivo,
                self.ancho,
                self.alto
            )
        )


        indicador = QLabel(
            estado_resolucion[
                "icono"
            ]
        )


        indicador.setAlignment(
            Qt.AlignCenter
        )


        indicador.setStyleSheet("""
            QLabel {
                font-size: 22px;
                padding: 2px 5px;
            }
        """)


        indicador.setToolTip(
            estado_resolucion[
                "tooltip"
            ]
        )


        fila_info.addWidget(
            indicador
        )


        layout.addLayout(
            fila_info
        )


        # ----------------------------------------------------
        # NOMBRE INDIVIDUAL
        # ----------------------------------------------------

        fila_nombre = QHBoxLayout()


        self.campo_prefijo = QLineEdit()

        self.campo_prefijo.setPlaceholderText(
            "Prefijo"
        )

        self.campo_prefijo.setText(
            prefijos_salida.get(
                self.archivo,
                ""
            )
        )


        self.campo_prefijo.textChanged.connect(
            self.cambio_prefijo
        )


        fila_nombre.addWidget(
            self.campo_prefijo
        )


        self.campo_sufijo = QLineEdit()

        self.campo_sufijo.setPlaceholderText(
            "Sufijo"
        )

        self.campo_sufijo.setText(
            sufijos_salida.get(
                self.archivo,
                ""
            )
        )


        self.campo_sufijo.textChanged.connect(
            self.cambio_sufijo
        )


        fila_nombre.addWidget(
            self.campo_sufijo
        )


        layout.addLayout(
            fila_nombre
        )


        # ----------------------------------------------------
        # CONTROLES
        # ----------------------------------------------------

        botones = QHBoxLayout()


        boton_auto = QPushButton(
            "↺ Automático"
        )


        boton_auto.clicked.connect(
            self.restaurar_automatico
        )


        botones.addWidget(
            boton_auto
        )


        boton_editor = QPushButton(
            "⛶ Editor"
        )


        boton_editor.clicked.connect(
            self.abrir_editor
        )


        botones.addWidget(
            boton_editor
        )


        layout.addLayout(
            botones
        )


        # ----------------------------------------------------
        # CHECKBOX IA
        # ----------------------------------------------------

        self.checkbox_ia = QCheckBox(
            "✨ Mejorar con IA"
        )


        self.checkbox_ia.setChecked(
            fotos_mejorar_ia.get(
                self.archivo,
                False
            )
        )


        self.checkbox_ia.toggled.connect(
            self.cambio_ia
        )


        layout.addWidget(
            self.checkbox_ia
        )


    # ========================================================
    # PREFIJO
    # ========================================================

    def cambio_prefijo(
        self,
        texto
    ):

        prefijos_salida[
            self.archivo
        ] = texto


    # ========================================================
    # SUFIJO
    # ========================================================

    def cambio_sufijo(
        self,
        texto
    ):

        sufijos_salida[
            self.archivo
        ] = texto


    # ========================================================
    # CHECKBOX IA
    # ========================================================

    def cambio_ia(
        self,
        marcado
    ):

        fotos_mejorar_ia[
            self.archivo
        ] = marcado

        actualizar_texto_boton_ia_todas()


    # ========================================================
    # GUARDAR AJUSTES
    # ========================================================

    def guardar_ajustes(
        self
    ):

        if (
            abs(self.offset_x)
            < 0.00001
            and
            abs(self.offset_y)
            < 0.00001
            and
            abs(self.zoom - 1.0)
            < 0.00001
        ):

            if self.archivo in (
                ajustes_manuales
            ):

                del ajustes_manuales[
                    self.archivo
                ]

            return


        ajustes_manuales[
            self.archivo
        ] = {
            "x": self.offset_x,
            "y": self.offset_y,
            "zoom": self.zoom
        }


    # ========================================================
    # PREVIEW
    # ========================================================

    def actualizar_preview(
        self
    ):

        try:

            resultado = generar_preview(
                self.archivo,
                self.ancho,
                self.alto
            )


            pixmap = pillow_a_pixmap(
                resultado
            )


            ancho_preview = max(
                200,
                tamano_miniatura
            )

            alto_preview = int(
                ancho_preview * 0.58
            )


            pixmap = pixmap.scaled(
                ancho_preview,
                alto_preview,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )


            self.preview.setFixedSize(
                ancho_preview,
                alto_preview
            )


            self.preview.setPixmap(
                pixmap
            )


        except Exception as error:

            print(
                "ERROR preview:"
            )

            print(
                error
            )


    # ========================================================
    # EDITOR GRANDE
    # ========================================================

    def abrir_editor(
        self
    ):

        editor = EditorGrande(
            self.archivo,
            self.ancho,
            self.alto,
            ventana
        )


        editor.exec()


        ajustes = ajustes_manuales.get(
            self.archivo,
            {
                "x": 0,
                "y": 0,
                "zoom": 1.0
            }
        )


        self.offset_x = (
            ajustes["x"]
        )

        self.offset_y = (
            ajustes["y"]
        )

        self.zoom = (
            ajustes["zoom"]
        )


        self.actualizar_preview()


    # ========================================================
    # AUTOMÁTICO
    # ========================================================

    def restaurar_automatico(
        self
    ):

        self.offset_x = 0

        self.offset_y = 0

        self.zoom = 1.0


        if self.archivo in (
            ajustes_manuales
        ):

            del ajustes_manuales[
                self.archivo
            ]


        self.actualizar_preview()


# ============================================================
# ACTUALIZAR BOTÓN IA
# ============================================================

def actualizar_texto_boton_ia_todas():

    if not archivos_seleccionados:

        boton_ia_todas.setText(
            "✨ IA: Seleccionar todas"
        )

        return


    todas_seleccionadas = all(
        fotos_mejorar_ia.get(
            archivo,
            False
        )
        for archivo in archivos_seleccionados
    )


    if todas_seleccionadas:

        boton_ia_todas.setText(
            "✨ IA: Deseleccionar todas"
        )

    else:

        boton_ia_todas.setText(
            "✨ IA: Seleccionar todas"
        )


# ============================================================
# ALTERNAR IA TODAS
# ============================================================

def alternar_ia_todas():

    if not archivos_seleccionados:

        return


    todas_seleccionadas = all(
        fotos_mejorar_ia.get(
            archivo,
            False
        )
        for archivo in archivos_seleccionados
    )


    nuevo_estado = (
        not todas_seleccionadas
    )


    for archivo in archivos_seleccionados:

        fotos_mejorar_ia[
            archivo
        ] = nuevo_estado


    for i in range(
        grid.count()
    ):

        item = grid.itemAt(
            i
        )

        widget = item.widget()


        if isinstance(
            widget,
            FotoEditor
        ):

            widget.checkbox_ia.blockSignals(
                True
            )

            widget.checkbox_ia.setChecked(
                nuevo_estado
            )

            widget.checkbox_ia.blockSignals(
                False
            )


    actualizar_texto_boton_ia_todas()


# ============================================================
# MOSTRAR FOTOS
# ============================================================

def mostrar_fotos():

    while grid.count():

        item = grid.takeAt(
            0
        )

        widget = item.widget()

        if widget:

            widget.deleteLater()


    ancho, alto = (
        formato.currentData()
    )


    cantidad = len(
        archivos_seleccionados
    )


    if cantidad == 0:

        return


    # --------------------------------------------------------
    # PROGRESO DE IMPORTACIÓN
    # --------------------------------------------------------

    progreso = QProgressDialog(
        "Preparando imágenes...",
        "",
        0,
        cantidad,
        ventana
    )


    progreso.setWindowTitle(
        "SmartCrop AI — Importando"
    )


    progreso.setWindowModality(
        Qt.WindowModal
    )


    progreso.setMinimumDuration(
        0
    )


    progreso.setAutoClose(
        False
    )


    progreso.setAutoReset(
        False
    )


    progreso.show()


    QApplication.processEvents()


    # --------------------------------------------------------
    # PREPARAR FOTOS
    # --------------------------------------------------------

    for numero, archivo in enumerate(
        archivos_seleccionados
    ):

        nombre = os.path.basename(
            archivo
        )


        progreso.setLabelText(
            "Analizando "
            +
            str(numero + 1)
            +
            " de "
            +
            str(cantidad)
            +
            ":\n"
            +
            nombre
        )


        progreso.setValue(
            numero
        )


        QApplication.processEvents()


        try:

            analizar_foto(
                archivo
            )


            tarjeta = FotoEditor(
                archivo,
                ancho,
                alto
            )


            columnas = max(
                1,
                int(
                    max(
                        1,
                        scroll.viewport().width()
                    )
                    /
                    (
                        tamano_miniatura
                        +
                        40
                    )
                )
            )


            fila = (
                numero //
                columnas
            )

            columna = (
                numero %
                columnas
            )


            grid.addWidget(
                tarjeta,
                fila,
                columna
            )


            QApplication.processEvents()


        except Exception as error:

            print(
                "ERROR preparando:"
            )

            print(
                archivo
            )

            print(
                error
            )


    progreso.setValue(
        cantidad
    )


    progreso.setLabelText(
        "Importación finalizada."
    )


    QApplication.processEvents()


    progreso.close()


    actualizar_texto_boton_ia_todas()


# ============================================================
# LIMPIAR LOTE ACTUAL
# ============================================================

def limpiar_todo():
    global archivos_seleccionados
    archivos_seleccionados = []
    analisis_cache.clear()
    ajustes_manuales.clear()
    fotos_mejorar_ia.clear()
    prefijos_salida.clear()
    sufijos_salida.clear()
    prefijo_global.clear()
    sufijo_global.clear()
    while grid.count():
        item = grid.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
    titulo.setText("SmartCrop AI — Seleccioná fotos para comenzar")
    actualizar_texto_boton_ia_todas()


# ============================================================
# SELECCIONAR FOTOS
# ============================================================

def seleccionar_fotos():

    global archivos_seleccionados


    archivos, _ = (
        QFileDialog.getOpenFileNames(
            ventana,
            "Seleccionar fotos",
            "",
            "Imágenes (*.jpg *.jpeg *.png *.webp *.avif)"
        )
    )


    if not archivos:

        return

    if not AVIF_DISPONIBLE and any(a.lower().endswith(".avif") for a in archivos):
        QMessageBox.warning(
            ventana, "Soporte AVIF no instalado",
            "Para importar AVIF instalá la dependencia con:\n\npip install pillow-avif-plugin\n\nLuego reiniciá SmartCrop AI. En el EXE también hay que incluir el plugin al compilar."
        )
        archivos = [a for a in archivos if not a.lower().endswith(".avif")]
        if not archivos:
            return


    archivos_seleccionados = (
        archivos
    )


    ajustes_manuales.clear()

    fotos_mejorar_ia.clear()

    prefijos_salida.clear()

    sufijos_salida.clear()


    actualizar_texto_boton_ia_todas()


    titulo.setText(
        "SmartCrop AI — "
        +
        str(
            len(archivos)
        )
        +
        " fotos"
    )


    mostrar_fotos()


# ============================================================
# VIGILANCIA AUTOMÁTICA DE CARPETA
# ============================================================

EXTENSIONES_IMAGEN = (".jpg", ".jpeg", ".png", ".webp", ".avif")


def elegir_carpeta_vigilada():
    global carpeta_monitoreada, archivos_vistos_carpeta
    carpeta = QFileDialog.getExistingDirectory(
        ventana, "Elegir carpeta para sincronizar", carpeta_monitoreada or ""
    )
    if not carpeta:
        return
    carpeta_monitoreada = os.path.abspath(carpeta)
    archivos_vistos_carpeta = set(archivos_seleccionados)
    archivos_pendientes_estabilidad.clear()
    boton_carpeta.setText("Carpeta: " + os.path.basename(carpeta_monitoreada))
    boton_detener_carpeta.setEnabled(True)
    # Detecta también imágenes que ya existían en la carpeta al seleccionarla.
    escanear_carpeta_vigilada()


def detener_vigilancia_carpeta():
    global carpeta_monitoreada
    carpeta_monitoreada = ""
    archivos_pendientes_estabilidad.clear()
    boton_carpeta.setText("Vigilar carpeta…")
    boton_detener_carpeta.setEnabled(False)


def escanear_carpeta_vigilada():
    global archivos_seleccionados
    if not carpeta_monitoreada or not os.path.isdir(carpeta_monitoreada):
        return
    try:
        rutas = [
            os.path.join(carpeta_monitoreada, nombre)
            for nombre in os.listdir(carpeta_monitoreada)
            if nombre.lower().endswith(EXTENSIONES_IMAGEN)
            and os.path.isfile(os.path.join(carpeta_monitoreada, nombre))
        ]
    except OSError:
        return

    ahora = time.time()
    nuevos_listos = []
    for ruta in rutas:
        ruta = os.path.abspath(ruta)
        if ruta in archivos_vistos_carpeta or ruta in archivos_seleccionados:
            continue
        try:
            tamano = os.path.getsize(ruta)
            anterior = archivos_pendientes_estabilidad.get(ruta)
            if anterior and anterior[0] == tamano and ahora - anterior[1] >= 1.5:
                # Tamaño estable: probablemente terminó de copiarse/guardarse.
                nuevos_listos.append(ruta)
                archivos_vistos_carpeta.add(ruta)
                archivos_pendientes_estabilidad.pop(ruta, None)
            else:
                archivos_pendientes_estabilidad[ruta] = (tamano, ahora)
        except OSError:
            continue

    if nuevos_listos:
        archivos_seleccionados.extend(nuevos_listos)
        titulo.setText(f"SmartCrop AI — {len(archivos_seleccionados)} fotos (carpeta sincronizada)")
        mostrar_fotos()


# Escaneo periódico para detectar archivos nuevos sin bloquear el programa.
timer_carpeta = QTimer(ventana)
timer_carpeta.setInterval(2000)
timer_carpeta.timeout.connect(escanear_carpeta_vigilada)
timer_carpeta.start()


# ============================================================
# CAMBIAR FORMATO
# ============================================================

def cambiar_formato():

    if not archivos_seleccionados:

        return


    ajustes_manuales.clear()


    mostrar_fotos()


# ============================================================
# CAMBIAR TAMAÑO MINIATURAS
# ============================================================

def cambiar_tamano_miniaturas(
    valor
):

    global tamano_miniatura

    tamano_miniatura = valor


    label_tamano_miniaturas.setText(
        f"{valor}px"
    )


    if not archivos_seleccionados:

        return


    mostrar_fotos()


# ============================================================
# APLICAR NOMBRES A TODAS
# ============================================================

def aplicar_nombres_a_todas():

    prefijo = (
        prefijo_global.text()
    )

    sufijo = (
        sufijo_global.text()
    )


    for archivo in archivos_seleccionados:

        prefijos_salida[
            archivo
        ] = prefijo

        sufijos_salida[
            archivo
        ] = sufijo


    # --------------------------------------------------------
    # Actualizar campos visualmente
    # --------------------------------------------------------

    for i in range(
        grid.count()
    ):

        item = grid.itemAt(
            i
        )

        widget = item.widget()


        if isinstance(
            widget,
            FotoEditor
        ):

            archivo = (
                widget.archivo
            )


            widget.campo_prefijo.blockSignals(
                True
            )

            widget.campo_prefijo.setText(
                prefijos_salida.get(
                    archivo,
                    ""
                )
            )

            widget.campo_prefijo.blockSignals(
                False
            )


            widget.campo_sufijo.blockSignals(
                True
            )

            widget.campo_sufijo.setText(
                sufijos_salida.get(
                    archivo,
                    ""
                )
            )

            widget.campo_sufijo.blockSignals(
                False
            )


# ============================================================
# EXPORTAR
# ============================================================

def exportar():

    if not archivos_seleccionados:

        QMessageBox.warning(
            ventana,
            "SmartCrop",
            "Primero seleccioná algunas fotos."
        )

        return


    ancho, alto = (
        formato.currentData()
    )


    escala_esrgan = (
        mejora_ia.currentData()
    )


    extension_salida = (
        formato_salida.currentData()
    )


    # --------------------------------------------------------
    # Fotos con IA
    # --------------------------------------------------------

    fotos_con_ia = [
        archivo
        for archivo in archivos_seleccionados
        if fotos_mejorar_ia.get(
            archivo,
            False
        )
    ]


    # --------------------------------------------------------
    # Comprobar Real-ESRGAN
    # --------------------------------------------------------

    if (
        escala_esrgan > 0
        and
        len(fotos_con_ia) > 0
    ):

        if not es_real_esrgan_disponible():

            QMessageBox.warning(
                ventana,
                "Real-ESRGAN no encontrado",
                "Hay fotos marcadas para "
                "mejora con IA, pero SmartCrop "
                "no encontró Real-ESRGAN.\n\n"
                "Ruta buscada:\n"
                +
                RUTA_ESRGAN
                +
                "\n\n"
                "Modelos buscados en:\n"
                +
                CARPETA_MODELOS
            )

            return


    # --------------------------------------------------------
    # Carpeta
    # --------------------------------------------------------

    carpeta = (
        QFileDialog.getExistingDirectory(
            ventana,
            "Elegir carpeta de destino"
        )
    )


    if not carpeta:

        return


    # --------------------------------------------------------
    # PROGRESO
    # --------------------------------------------------------

    progreso = QProgressDialog(
        "Preparando exportación...",
        "Cancelar",
        0,
        len(
            archivos_seleccionados
        ),
        ventana
    )


    progreso.setWindowTitle(
        "SmartCrop AI — Exportando"
    )


    progreso.setWindowModality(
        Qt.WindowModal
    )


    progreso.show()


    cantidad = 0

    cancelado = False


    # --------------------------------------------------------
    # EXPORTAR
    # --------------------------------------------------------

    for numero, archivo in enumerate(
        archivos_seleccionados
    ):

        if progreso.wasCanceled():

            cancelado = True

            break


        nombre = os.path.basename(
            archivo
        )


        usar_ia = (
            escala_esrgan > 0
            and
            fotos_mejorar_ia.get(
                archivo,
                False
            )
        )


        if usar_ia:

            texto = (
                "✨ Mejorando con IA: "
                +
                nombre
            )

        else:

            texto = (
                "Exportando: "
                +
                nombre
            )


        progreso.setLabelText(
            texto
        )


        QApplication.processEvents()


        try:

            procesar_exportacion(
                archivo,
                ancho,
                alto,
                escala_esrgan
                if usar_ia
                else 0,
                carpeta,
                extension_salida
            )


            cantidad += 1


        except Exception as error:

            print()
            print(
                "ERROR:"
            )

            print(
                archivo
            )

            print(
                error
            )


            QMessageBox.warning(
                ventana,
                "Error",
                "No se pudo procesar:\n\n"
                +
                nombre
                +
                "\n\n"
                +
                str(error)
            )


        progreso.setValue(
            numero + 1
        )


        QApplication.processEvents()


    progreso.close()


    # --------------------------------------------------------
    # SONIDO DE WINDOWS
    # --------------------------------------------------------

    if (
        cantidad > 0
        and
        not cancelado
    ):

        try:

            winsound.MessageBeep(
                winsound.MB_ICONASTERISK
            )

        except:

            pass


    # --------------------------------------------------------
    # RESUMEN
    # --------------------------------------------------------

    if cantidad > 0:

        cantidad_ia = sum(
            1
            for archivo
            in archivos_seleccionados
            if (
                fotos_mejorar_ia.get(
                    archivo,
                    False
                )
                and
                escala_esrgan > 0
            )
        )


        mensaje = (
            "Se procesaron "
            +
            str(cantidad)
            +
            " imágenes."
        )


        if cantidad_ia > 0:

            mensaje += (
                "\n\n"
                "Mejoradas con IA: "
                +
                str(cantidad_ia)
            )


        mensaje += (
            "\n\n"
            "Formato: "
            +
            extension_salida.upper()
        )


        if cancelado:

            mensaje += (
                "\n\n"
                "La exportación fue cancelada."
            )


        QMessageBox.information(
            ventana,
            "SmartCrop",
            mensaje
        )


# ============================================================
# CONEXIONES
# ============================================================

boton_seleccionar.clicked.connect(
    seleccionar_fotos
)

boton_carpeta.clicked.connect(elegir_carpeta_vigilada)
boton_detener_carpeta.clicked.connect(detener_vigilancia_carpeta)
boton_limpiar.clicked.connect(limpiar_todo)

formato.currentIndexChanged.connect(
    cambiar_formato
)

boton_ia_todas.clicked.connect(
    alternar_ia_todas
)

boton_exportar.clicked.connect(
    exportar
)

boton_aplicar_nombres.clicked.connect(
    aplicar_nombres_a_todas
)

slider_miniaturas.valueChanged.connect(
    cambiar_tamano_miniaturas
)

boton_menos.clicked.connect(
    lambda: slider_miniaturas.setValue(
        max(
            slider_miniaturas.minimum(),
            slider_miniaturas.value() - 50
        )
    )
)

boton_mas.clicked.connect(
    lambda: slider_miniaturas.setValue(
        min(
            slider_miniaturas.maximum(),
            slider_miniaturas.value() + 50
        )
    )
)


# ============================================================
# INICIAR
# ============================================================

ventana.show()

sys.exit(
    app.exec()
)