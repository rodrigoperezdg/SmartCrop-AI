#define MyAppName "SmartCrop AI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Rodrigo Pérez"
#define MyAppExeName "SmartCrop.exe"

[Setup]
AppId={{D673E15A-9B31-4BC2-9230-6E5A58C89A11}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

; ============================================================
; INSTALACIÓN SIN ADMINISTRADOR
; ============================================================

PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Se instala solamente para el usuario actual.
; No utiliza Program Files.
DefaultDirName={localappdata}\Programs\SmartCrop AI

DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; ============================================================
; INSTALADOR GENERADO
; ============================================================

OutputDir=installer
OutputBaseFilename=SmartCrop_Setup_1.0.0

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

; ============================================================
; DESINSTALADOR
; ============================================================

UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\SmartCrop.exe

; ============================================================
; COMPATIBILIDAD
; ============================================================

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; ============================================================
; INTERFAZ
; ============================================================

SetupLogging=yes
ShowLanguageDialog=no

[Languages]

Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"


; ============================================================
; ARCHIVOS DE SMARTCROP
; ============================================================

[Files]

; Copia TODO lo generado por PyInstaller.
; Esto incluye:
;
; SmartCrop.exe
; _internal\
; Real-ESRGAN
; models
; YOLO
; Pillow AVIF
; OpenCV
; PySide6
; etc.

Source: "dist\SmartCrop\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs


; ============================================================
; ACCESOS DIRECTOS
; ============================================================

[Icons]

; Menú Inicio
Name: "{autoprograms}\SmartCrop AI"; Filename: "{app}\SmartCrop.exe"; WorkingDir: "{app}"

; Escritorio (opcional)
Name: "{autodesktop}\SmartCrop AI"; Filename: "{app}\SmartCrop.exe"; WorkingDir: "{app}"; Tasks: desktopicon


; ============================================================
; OPCIONES DEL INSTALADOR
; ============================================================

[Tasks]

Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked


; ============================================================
; EJECUTAR AL TERMINAR
; ============================================================

[Run]

Filename: "{app}\SmartCrop.exe"; Description: "Ejecutar SmartCrop AI"; Flags: nowait postinstall skipifsilent