# Empaqueta una compilacion PyInstaller ya existente en un MSIX SIN FIRMA.
# No modifica el MSIX certificado ni su directorio Package_Final.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$AppDir,
    [Parameter(Mandatory = $true)][string]$TemplateDir,
    [Parameter(Mandatory = $true)][string]$OutputDir,
    [string]$OutputName = 'SmartCropAI_Rebuild_Unsigned.msix',
    [string]$AssetsDir,
    [string]$MakeAppxPath
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Resolve-ExistingDirectory([string]$Path, [string]$Description) {
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "$Description no existe: $Path"
    }
    return (Resolve-Path -LiteralPath $Path).ProviderPath
}

$app = Resolve-ExistingDirectory $AppDir 'AppDir'
$template = Resolve-ExistingDirectory $TemplateDir 'TemplateDir'
if (-not (Test-Path -LiteralPath (Join-Path $app 'SmartCrop.exe') -PathType Leaf)) { throw 'Falta SmartCrop.exe en AppDir.' }
if (-not (Test-Path -LiteralPath (Join-Path $app '_internal') -PathType Container)) { throw 'Falta _internal en AppDir.' }
if (-not (Test-Path -LiteralPath (Join-Path $template 'AppxManifest.xml') -PathType Leaf)) { throw 'Falta AppxManifest.xml en TemplateDir.' }
# Compatibilidad: si no se indica AssetsDir, usar Assets de la plantilla
# o la carpeta Assets hermana de MSIX_Template dentro del repositorio.
if ([string]::IsNullOrWhiteSpace($AssetsDir)) {
    $templateAssets = Join-Path $template 'Assets'
    if (Test-Path -LiteralPath $templateAssets -PathType Container) {
        $AssetsDir = $templateAssets
    } else {
        $AssetsDir = Join-Path (Split-Path -Parent $template) 'Assets'
    }
}
$assets = Resolve-ExistingDirectory $AssetsDir 'AssetsDir'
if ([IO.Path]::GetFileName($OutputName) -ne $OutputName -or -not $OutputName.EndsWith('.msix', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'OutputName debe ser un nombre de archivo .msix, sin carpetas.'
}

if ([string]::IsNullOrWhiteSpace($MakeAppxPath)) {
    $sdkRoot = Join-Path ${env:ProgramFiles(x86)} 'Windows Kits\10\bin'
    if (-not (Test-Path -LiteralPath $sdkRoot)) { throw 'No se encontro Windows SDK (Windows Kits\10\bin).' }
    $candidate = Get-ChildItem -LiteralPath $sdkRoot -Directory | Sort-Object { try { [version]$_.Name } catch { [version]'0.0' } } -Descending |
        ForEach-Object { Join-Path $_.FullName 'x64\makeappx.exe' } |
        Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
    if (-not $candidate) { throw 'No se encontro makeappx.exe x64 en Windows SDK.' }
    $MakeAppxPath = $candidate
}
if (-not (Test-Path -LiteralPath $MakeAppxPath -PathType Leaf)) { throw "MakeAppx no existe: $MakeAppxPath" }

$outFull = [IO.Path]::GetFullPath($ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDir))
$root = [IO.Path]::GetPathRoot($outFull)
if ($outFull.TrimEnd('\') -eq $root.TrimEnd('\')) { throw 'OutputDir no puede ser la raiz de una unidad.' }
foreach ($protected in @($app, $template, $assets)) {
    if ($outFull.TrimEnd('\').Equals($protected.TrimEnd('\'), [StringComparison]::OrdinalIgnoreCase) -or
        $outFull.StartsWith($protected.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase) -or
        $protected.StartsWith($outFull.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'OutputDir debe estar separado de AppDir y TemplateDir.'
    }
}
if (-not (Test-Path -LiteralPath $outFull)) { New-Item -ItemType Directory -Path $outFull | Out-Null }
$target = Join-Path $outFull $OutputName
if (Test-Path -LiteralPath $target) { throw "Ya existe el paquete de salida (no se sobrescribe): $target" }
$staging = Join-Path $outFull ('staging_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $staging | Out-Null
try {
    Copy-Item -LiteralPath (Join-Path $template 'AppxManifest.xml') -Destination $staging
    Copy-Item -LiteralPath $assets -Destination (Join-Path $staging 'Assets') -Recurse
    Copy-Item -LiteralPath (Join-Path $app 'SmartCrop.exe') -Destination $staging
    Copy-Item -LiteralPath (Join-Path $app '_internal') -Destination $staging -Recurse

    [xml]$manifest = Get-Content -LiteralPath (Join-Path $staging 'AppxManifest.xml') -Raw -Encoding UTF8
    $ns = New-Object System.Xml.XmlNamespaceManager($manifest.NameTable)
    $ns.AddNamespace('p', 'http://schemas.microsoft.com/appx/manifest/foundation/windows10')
    $identity = $manifest.SelectSingleNode('/p:Package/p:Identity', $ns)
    if (-not $identity) { throw 'Manifiesto invalido: falta Identity.' }
    if ($identity.GetAttribute('ProcessorArchitecture') -ne 'x64') { throw 'El manifiesto no declara arquitectura x64.' }
    $requiredAssets = @('StoreLogo.png','Square150x150Logo.png','Square44x44Logo.png','Wide310x150Logo.png','Square310x310Logo.png','Square71x71Logo.png')
    foreach ($asset in $requiredAssets) {
        if (-not (Test-Path -LiteralPath (Join-Path $staging "Assets\$asset") -PathType Leaf)) { throw "Falta recurso del manifiesto: Assets\$asset" }
    }
    Write-Host "Identidad: $($identity.GetAttribute('Name'))"
    Write-Host "Version:   $($identity.GetAttribute('Version'))"
    Write-Warning 'Se generara un MSIX SIN FIRMA. No instalar ni publicar sin revisar identidad, version, licencias y firma.'
    & $MakeAppxPath pack /d $staging /p $target
    if ($LASTEXITCODE -ne 0) { throw "MakeAppx fallo con codigo $LASTEXITCODE" }
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw 'MakeAppx no genero el paquete.' }
    Write-Host "MSIX sin firmar creado: $target"
    Get-FileHash -LiteralPath $target -Algorithm SHA256 | Format-List
}
finally {
    if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }
}
