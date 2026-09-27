$ErrorActionPreference = 'Stop'
$hunterRoot = $PSScriptRoot
$hunterPython = Join-Path $hunterRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $hunterPython)) {
    throw 'Create .venv and install requirements.txt first; see README.md.'
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
