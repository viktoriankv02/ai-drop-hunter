$ErrorActionPreference = 'Stop'
$hunterRoot = $PSScriptRoot
$hunterPython = Join-Path $hunterRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $hunterPython)) {
    throw 'Create .venv and install requirements.txt first; see README.md.'
}
# Start the already installed local model service; never download models here.
try {
    Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2 | Out-Null
} catch {
    $hunterOllama = 'D:\AI\Ollama\ollama.exe'
    $hunterModels = [Environment]::GetEnvironmentVariable('OLLAMA_MODELS','User')
    if ((Test-Path -LiteralPath $hunterOllama) -and $hunterModels -and (Test-Path -LiteralPath $hunterModels)) {
        $env:OLLAMA_MODELS = $hunterModels
        $env:OLLAMA_HOST = '127.0.0.1:11434'
        $hunterModelLogs = Join-Path $hunterRoot 'data'
        New-Item -ItemType Directory -Path $hunterModelLogs -Force | Out-Null
        Start-Process -FilePath $hunterOllama -ArgumentList 'serve' -WindowStyle Hidden -RedirectStandardOutput (Join-Path $hunterModelLogs 'ollama.log') -RedirectStandardError (Join-Path $hunterModelLogs 'ollama-error.log') | Out-Null
    } else {
        Write-Warning 'Ollama or its configured model directory is unavailable. Discovery can run; analysis needs Ollama.'
    }
}
try {
    $hunterSession = Invoke-RestMethod -Uri 'http://127.0.0.1:4318/api/session' -TimeoutSec 2
    if ($hunterSession.mode -eq 'local') {
        Write-Output 'Hunter is already running: http://127.0.0.1:4318/'
        return
    }
} catch { }
$hunterData = Join-Path $hunterRoot 'data'
New-Item -ItemType Directory -Path $hunterData -Force | Out-Null
$hunterProcess = Start-Process -FilePath $hunterPython -ArgumentList 'main.py' -WorkingDirectory $hunterRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $hunterData 'server.log') -RedirectStandardError (Join-Path $hunterData 'server-error.log') -PassThru
for ($hunterAttempt=0; $hunterAttempt -lt 20; $hunterAttempt++) {
    Start-Sleep -Milliseconds 500
    try {
        $hunterSession = Invoke-RestMethod -Uri 'http://127.0.0.1:4318/api/session' -TimeoutSec 2
        if ($hunterSession.mode -eq 'local') {
            Write-Output 'Hunter is running: http://127.0.0.1:4318/'
            return
        }
    } catch { }
    if ($hunterProcess.HasExited) { break }
}
throw ('Hunter failed to start. Check ' + (Join-Path $hunterData 'server-error.log'))
