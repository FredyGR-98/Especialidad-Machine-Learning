param(
    [Parameter(Mandatory = $true)]
    [string]$PbixPath,

    [string[]]$RefreshSequences = @("HR", "IR", "HA", "IA"),

    [int]$OpenDelaySeconds = 10,
    [int]$FocusDelaySeconds = 2
)

if (-not (Test-Path -LiteralPath $PbixPath)) {
    throw "No se encontro el archivo PBIX en la ruta indicada: $PbixPath"
}

Start-Process -FilePath $PbixPath
Start-Sleep -Seconds $OpenDelaySeconds

$shell = New-Object -ComObject WScript.Shell
$activated = $shell.AppActivate("Power BI Desktop")

if (-not $activated) {
    throw "No fue posible enfocar Power BI Desktop para enviar la secuencia de actualizacion."
}

Start-Sleep -Seconds $FocusDelaySeconds

foreach ($sequence in $RefreshSequences) {
    $shell.SendKeys("%")
    Start-Sleep -Milliseconds 600
    $shell.SendKeys($sequence)
    Start-Sleep -Milliseconds 900
}
