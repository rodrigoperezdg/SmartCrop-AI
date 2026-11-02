#define MyAppName "SmartCrop AI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Rodrigo Pérez"
#define MyAppExeName "SmartCrop.exe"

[Setup]
AppId={{D673E15A-9B31-4BC2-9230-6E5A58C89A11}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
DefaultDirName={localappdata}\Programs\SmartCrop AI
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
; Candidato RC2: conserva intactos los instaladores previamente validados.
OutputBaseFilename=SmartCrop_Setup_1.0.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\SmartCrop.exe
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupLogging=yes
ShowLanguageDialog=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "dist\SmartCrop\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Copia temporal: se ejecuta solo si falta una version suficiente del runtime.
Source: "redist\vc_redist.x64.exe"; Flags: dontcopy

[Icons]
Name: "{autoprograms}\SmartCrop AI"; Filename: "{app}\SmartCrop.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\SmartCrop AI"; Filename: "{app}\SmartCrop.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Run]
Filename: "{app}\SmartCrop.exe"; Description: "Ejecutar SmartCrop AI"; Flags: nowait postinstall skipifsilent

[Code]
const
  VCRuntimeKey = 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64';
  { Version del paquete incluido: 14.44.35211.0. No afirma ser el minimo universal de SmartCrop. }
  RequiredMajor = 14;
  RequiredMinor = 44;
  RequiredBuild = 35211;

function HasCompatibleVCRuntime(): Boolean;
var
  Installed, Major, Minor, Build: Cardinal;
begin
  Result := False;
  if not RegQueryDWordValue(HKLM64, VCRuntimeKey, 'Installed', Installed) then Exit;
  if Installed <> 1 then Exit;
  if not RegQueryDWordValue(HKLM64, VCRuntimeKey, 'Major', Major) then Exit;
  if not RegQueryDWordValue(HKLM64, VCRuntimeKey, 'Minor', Minor) then Exit;
  if not RegQueryDWordValue(HKLM64, VCRuntimeKey, 'Bld', Build) then Exit;
  Result := (Major > RequiredMajor) or
    ((Major = RequiredMajor) and
      ((Minor > RequiredMinor) or
       ((Minor = RequiredMinor) and (Build >= RequiredBuild))));
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ExitCode: Integer;
  Launched: Boolean;
begin
  Result := '';
  if HasCompatibleVCRuntime() then begin
    Log('Microsoft Visual C++ x64 compatible detectado; se omite su instalacion.');
    Exit;
  end;

  if MsgBox('SmartCrop AI necesita Microsoft Visual C++ Redistributable x64.' + #13#10 + #13#10 +
      'No se encontro una version compatible. Se ejecutara el instalador oficial de Microsoft ' +
      '(puede solicitar permisos de administrador).' + #13#10 + #13#10 +
      '¿Deseas continuar?', mbConfirmation, MB_YESNO) <> IDYES then begin
    Result := 'No se autorizo la instalacion del requisito Microsoft Visual C++ Redistributable x64.';
    Exit;
  end;

  ExtractTemporaryFile('vc_redist.x64.exe');
  Launched := ShellExec('runas', ExpandConstant('{tmp}\vc_redist.x64.exe'),
    '/install /passive /norestart', '', SW_SHOWNORMAL, ewWaitUntilTerminated, ExitCode);

  if not Launched then begin
    Result := 'No se pudo iniciar el instalador de Microsoft Visual C++ (error ' + IntToStr(ExitCode) + ').';
    Exit;
  end;

  { 3010 indica que Microsoft requiere reinicio. 1638 puede indicar otra version instalada. }
  if (ExitCode <> 0) and (ExitCode <> 3010) and (ExitCode <> 1638) then begin
    Result := 'La instalacion de Microsoft Visual C++ no finalizo correctamente (codigo ' + IntToStr(ExitCode) + ').';
    Exit;
  end;

  if not HasCompatibleVCRuntime() then begin
    Result := 'No se pudo verificar una version compatible de Microsoft Visual C++ x64 tras su instalacion.';
    Exit;
  end;

  { Inno Setup solicitara reiniciar antes de continuar con la instalacion de SmartCrop. }
  if ExitCode = 3010 then begin
    Log('Visual C++ instalado: Windows requiere reiniciar antes de continuar.');
    NeedsRestart := True;
  end;
end;

