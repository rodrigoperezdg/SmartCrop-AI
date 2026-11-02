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
; Prueba online: Visual C++ se descarga desde Microsoft.
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
  ScriptPath, DownloadPath, ScriptText: String;
begin
  Result := '';
  if HasCompatibleVCRuntime() then begin
    Log('Microsoft Visual C++ x64 compatible detectado; se omite su instalacion.');
    Exit;
  end;

  if MsgBox('SmartCrop AI necesita Microsoft Visual C++ Redistributable x64.' + #13#10 + #13#10 +
      'No se encontro una version compatible. Se descargara y ejecutara el instalador oficial de Microsoft ' +
      '(puede solicitar permisos de administrador).' + #13#10 + #13#10 +
      '¿Deseas continuar?', mbConfirmation, MB_YESNO) <> IDYES then begin
    Result := 'No se autorizo la instalacion del requisito Microsoft Visual C++ Redistributable x64.';
    Exit;
  end;

  DownloadPath := ExpandConstant('{tmp}\vc_redist.x64.exe');
  ScriptPath := ExpandConstant('{tmp}\smartcrop_download_vc.ps1');
  ScriptText :=
    '$ErrorActionPreference = ''Stop''' + #13#10 +
    '[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12' + #13#10 +
    '$url = ''https://aka.ms/vc14/vc_redist.x64.exe''' + #13#10 +
    '$dest = ''' + DownloadPath + '''' + #13#10 +
    'try {' + #13#10 +
    '  Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing -MaximumRedirection 10' + #13#10 +
    '  if ((Get-Item $dest).Length -lt 1000000) { throw ''Descarga incompleta'' }' + #13#10 +
    '  $sig = Get-AuthenticodeSignature -FilePath $dest' + #13#10 +
    '  if ($sig.Status -ne ''Valid'' -or $null -eq $sig.SignerCertificate -or ' +
      '$sig.SignerCertificate.Subject -notmatch ''Microsoft Corporation'') { ' +
      'throw ''Firma digital de Microsoft no valida'' }' + #13#10 +
    '  exit 0' + #13#10 +
    '} catch { Write-Error $_; exit 1 }' + #13#10;
  if not SaveStringToFile(ScriptPath, ScriptText, False) then begin
    Result := 'No se pudo preparar la descarga de Microsoft Visual C++.';
    Exit;
  end;
  Log('Descargando Visual C++ x64 desde Microsoft y verificando su firma digital.');
  Launched := Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'),
    '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + ScriptPath + '"',
    '', SW_HIDE, ewWaitUntilTerminated, ExitCode);
  if (not Launched) or (ExitCode <> 0) then begin
    Result := 'No se pudo descargar o verificar Microsoft Visual C++ x64. ' +
      'Comprueba la conexion a Internet y vuelve a intentarlo.';
    Exit;
  end;
  Launched := ShellExec('runas', DownloadPath,
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

