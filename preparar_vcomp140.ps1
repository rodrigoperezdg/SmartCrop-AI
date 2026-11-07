$ErrorActionPreference = "Stop"

$raizBuildTools = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"
$carpetaSalida = Join-Path $PSScriptRoot "dist\SmartCrop\_internal"

if (!(Test-Path $carpetaSalida)) {
    throw "No existe dist\SmartCrop\_internal. Primero hay que compilar SmartCrop."
}

$raizRedist = Join-Path $raizBuildTools "VC\Redist\MSVC"

if (!(Test-Path $raizRedist)) {
    throw "No se encontró la carpeta de redistribución de Microsoft."
}

$dll = Get-ChildItem $raizRedist -Filter "vcomp140.dll" -Recurse -File |
    Where-Object {
        $_.FullName -match '\\x64\\Microsoft\.VC143\.OpenMP\\vcomp140\.dll$'
    } |
    Sort-Object FullName -Descending |
    Select-Object -First 1

if (!$dll) {
    throw "No se encontró VCOMP140.DLL x64 en Microsoft Build Tools."
}

$firma = Get-AuthenticodeSignature $dll.FullName

if ($firma.Status -ne "Valid") {
    throw "La firma de la DLL no es válida."
}

if ($dll.VersionInfo.FileVersion -ne "14.44.35211.0") {
    throw "La versión de la DLL no coincide con la verificada."
}

$hashOrigen = (Get-FileHash $dll.FullName -Algorithm SHA256).Hash
if ($hashOrigen -ne "55ABA23CDCD6484FBB06F4155B8CA75ADFCE7A881F10AFD0C49457165E677164") { throw "El SHA-256 de origen no coincide con el verificado." }

$destino = Join-Path $carpetaSalida "VCOMP140.DLL"

Copy-Item $dll.FullName $destino -Force

$hash = (Get-FileHash $destino -Algorithm SHA256).Hash

if ($hash -ne "55ABA23CDCD6484FBB06F4155B8CA75ADFCE7A881F10AFD0C49457165E677164") { throw "El SHA-256 de VCOMP140.DLL no coincide con el verificado." }

Write-Host "`nDLL preparada correctamente."
Write-Host "Origen:  $($dll.FullName)"
Write-Host "Destino: $destino"
Write-Host "Versión: $((Get-Item $destino).VersionInfo.FileVersion)"
Write-Host "SHA256:  $hash"
