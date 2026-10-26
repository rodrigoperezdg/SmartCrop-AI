$ErrorActionPreference = "Stop"

$url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip"

$hashZipEsperado = "ABC02804E17982A3BF33675E4D471F91FA374E65B70167ABC09F31ACB412802D"
$hashExeEsperado = "07E49F7CBB4EDE01AE4DD4C399D3A7E5846E3D2085C3128EFF881E55CB7B1A0C"

$destino = Join-Path $PSScriptRoot "realesrgan-ncnn-vulkan.exe"
$zipTemporal = Join-Path ([System.IO.Path]::GetTempPath()) ("smartcrop-realesrgan-" + [guid]::NewGuid().ToString("N") + ".zip")

try {
    Write-Host "Descargando Real-ESRGAN..."
    Invoke-WebRequest -Uri $url -OutFile $zipTemporal

    $hashZip = (Get-FileHash $zipTemporal -Algorithm SHA256).Hash

    if ($hashZip -ne $hashZipEsperado) {
        throw "El SHA-256 del ZIP no coincide con el esperado."
    }

    Add-Type -AssemblyName System.IO.Compression.FileSystem

    $archivoZip = [System.IO.Compression.ZipFile]::OpenRead($zipTemporal)

    try {
        $entrada = $archivoZip.GetEntry("realesrgan-ncnn-vulkan.exe")

        if ($null -eq $entrada) {
            throw "No se encontro el ejecutable dentro del ZIP."
        }

        $exeTemporal = "$destino.tmp"

        [System.IO.Compression.ZipFileExtensions]::ExtractToFile(
            $entrada,
            $exeTemporal,
            $true
        )
    }
    finally {
        $archivoZip.Dispose()
    }

    $hashExe = (Get-FileHash $exeTemporal -Algorithm SHA256).Hash

    if ($hashExe -ne $hashExeEsperado) {
        throw "El SHA-256 del ejecutable no coincide con el esperado."
    }

    Move-Item -Path $exeTemporal -Destination $destino -Force

    Write-Host "Real-ESRGAN preparado y verificado correctamente."
    Write-Host "Archivo: $destino"
}
finally {
    Remove-Item $zipTemporal -Force -ErrorAction SilentlyContinue
}
