# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files

datas = [('yolo11n.pt', '.'), ('models/realesrgan-x4plus.bin', 'models'), ('models/realesrgan-x4plus.param', 'models')]
datas += collect_data_files('cv2', includes=['data/*'])
# Documentacion legal incluida en la distribucion.
datas += [
    ('LICENSE', 'licenses'),
    ('LICENSE-Real-ESRGAN.txt', 'licenses'),
    ('THIRD_PARTY_NOTICES.md', 'licenses'),
    ('LICENSE-LGPL-3.0.txt', 'licenses'),
    ('LICENSE-GPL-3.0.txt', 'licenses'),
    ('QT_LGPL_COMPLIANCE.md', 'licenses'),
    ('LEGAL_TERCEROS', 'licenses/LEGAL_TERCEROS'),
]

binaries = [('realesrgan-ncnn-vulkan.exe', '.')]
hiddenimports = []
tmp_ret = collect_all('torch')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('torchvision')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Incluir soporte HEIF/HEIC en la compilacion
tmp_ret = collect_all('pi_heif')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
    'PySide6.QtVirtualKeyboard',
    'PySide6.QtPdf',
    'PySide6.QtPdfWidgets',
    'PySide6.QtQml',
    'PySide6.QtQuick',
    'PySide6.QtQuickWidgets',
    'PySide6.QtNetwork',
],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SmartCrop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
# Excluir bibliotecas Qt de esta compilacion de prueba.
# Conservar la copia de seguridad funcional.
# ATENCION: verificar que la aplicacion inicia y exporta correctamente.
qt_excluir = {
    "Qt6VirtualKeyboard.dll",
    "Qt6Pdf.dll",
    "Qt6Qml.dll",
    "Qt6QmlMeta.dll",
    "Qt6QmlModels.dll",
    "Qt6QmlWorkerScript.dll",
    "Qt6Quick.dll",
    "qpdf.dll",
    "qtvirtualkeyboardplugin.dll",
}

a.binaries = [
    item for item in a.binaries
    if item[0].replace("\\", "/").split("/")[-1]
    not in qt_excluir
]
a.datas = [
    item for item in a.datas
    if item[0].replace("\\", "/").split("/")[-1]
    not in qt_excluir
]

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SmartCrop',
)
