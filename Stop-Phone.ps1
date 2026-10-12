$ErrorActionPreference = 'Stop'
$phoneRoot = $PSScriptRoot
& (Join-Path $phoneRoot '.venv\Scripts\python.exe') (Join-Path $phoneRoot 'scripts\phone_support.py') disable
$phoneFile = Join-Path $phoneRoot 'data\phone-processes.json'
if (Test-Path -LiteralPath $phoneFile) {
    $phoneState = Get-Content -LiteralPath $phoneFile -Raw | ConvertFrom-Json
    $phoneProcess = Get-CimInstance Win32_Process -Filter ('ProcessId=' + [int]$phoneState.tunnelPid)
    if ($phoneState.provider -eq 'localhost-run') {
        $phoneSsh = (Get-Command ssh.exe).Source
        if ($phoneProcess -and $phoneProcess.ExecutablePath -eq $phoneSsh -and $phoneProcess.CommandLine -like '*-R 80:127.0.0.1:4320 nokey@localhost.run*' -and $phoneProcess.CommandLine.Contains((Join-Path $phoneRoot 'data\phone-known-hosts'))) { Stop-Process -Id $phoneProcess.ProcessId }
    }
    $phoneExpected = [IO.Path]::GetFullPath((Join-Path $phoneRoot 'data\tools\cloudflared.exe'))
    if ($phoneProcess -and $phoneProcess.ExecutablePath -eq $phoneExpected -and $phoneProcess.CommandLine -like '*--url http://127.0.0.1:4320*') {
        Stop-Process -Id $phoneProcess.ProcessId
    }
}
Write-Output 'Phone sessions revoked. Managed tunnel stopped; local Hunter stays available.'
