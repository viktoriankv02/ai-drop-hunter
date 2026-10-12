$ErrorActionPreference = 'Stop'
$hunterRoot = $PSScriptRoot
$startScript = Join-Path $hunterRoot 'Start-Hunter.ps1'

try {
    $session = Invoke-RestMethod -Uri 'http://127.0.0.1:4318/api/session' -TimeoutSec 3
} catch {
    & $startScript
    $session = Invoke-RestMethod -Uri 'http://127.0.0.1:4318/api/session' -TimeoutSec 5
}

$headers = @{
    Origin = 'http://127.0.0.1:4318'
    'X-Hunter-Session' = $session.token
}
$result = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:4318/api/discovery/run' -Headers $headers -ContentType 'application/json' -Body '{}'
Write-Output ('Пошук поставлено в чергу. Джерел: ' + $result.job_ids.Count)
Write-Output "Результат з'явиться у вебдодатку: Знайдені проєкти → Останній пошук або Команда агентів."
