param([ValidateSet('cloudflare','localhost-run')][string]$Provider = 'cloudflare')
$ErrorActionPreference = 'Stop'
$phoneRoot = $PSScriptRoot
$phonePython = Join-Path $phoneRoot '.venv\Scripts\python.exe'
$phoneHelper = Join-Path $phoneRoot 'scripts\phone_support.py'
Push-Location $phoneRoot
try {
    & (Join-Path $phoneRoot 'Start-Hunter.ps1')
    $phoneState = (& $phonePython $phoneHelper status | ConvertFrom-Json)
    if ($phoneState.gateway_ready -and $phoneState.origin) {
        try {
            $phoneResponse = Invoke-WebRequest -Uri ($phoneState.origin + '/mobile-login') -TimeoutSec 10
            if ($phoneResponse.StatusCode -eq 200 -and $phoneResponse.Content.Contains('Hunter')) {
                Write-Output ('Phone access is running: ' + $phoneState.origin)
                return
            }
        } catch { }
    }
    & (Join-Path $phoneRoot 'Stop-Phone.ps1')
    if ($Provider -eq 'cloudflare') {
        Write-Output 'Preparing verified Cloudflare connector on D...'
        $phoneConnector = & $phonePython $phoneHelper download
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $phoneConnector)) { throw 'Connector download failed' }
        $phoneArguments = 'tunnel --no-autoupdate --protocol http2 --url http://127.0.0.1:4320'
    } else {
        $phoneConnector = (Get-Command ssh.exe -ErrorAction Stop).Source
        $phoneHosts = Join-Path $phoneRoot 'data\phone-known-hosts'
        $phoneArguments = '-T -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes -o IdentitiesOnly=yes -o IdentityFile=none -o IdentityAgent=none -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="' + $phoneHosts + '" -R 80:127.0.0.1:4320 nokey@localhost.run'
    }
    $phoneGateway = Get-NetTCPConnection -LocalPort 4320 -State Listen -ErrorAction SilentlyContinue
    if ($phoneGateway) {
        $phoneOwner = Get-CimInstance Win32_Process -Filter ('ProcessId=' + $phoneGateway[0].OwningProcess)
        if ($phoneOwner.CommandLine -notlike '*web_tma.backend.mobile_gateway*') { throw 'Port 4320 is used by another application' }
    } else {
        Start-Process -FilePath $phonePython -ArgumentList '-m web_tma.backend.mobile_gateway' -WorkingDirectory $phoneRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $phoneRoot 'data\phone-gateway.log') -RedirectStandardError (Join-Path $phoneRoot 'data\phone-gateway-error.log') | Out-Null
    }
    $phoneStamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $phoneLog = Join-Path $phoneRoot ('data\phone-tunnel-' + $phoneStamp + '.log')
    $phoneTunnel = Start-Process -FilePath $phoneConnector -ArgumentList $phoneArguments -WorkingDirectory $phoneRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $phoneRoot ('data\phone-tunnel-' + $phoneStamp + '-out.log')) -RedirectStandardError $phoneLog -PassThru
    @{ tunnelPid=$phoneTunnel.Id; connector=$phoneConnector; log=$phoneLog; provider=$Provider } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $phoneRoot 'data\phone-processes.json')
    for ($phoneAttempt=0; $phoneAttempt -lt 90; $phoneAttempt++) {
        if (Test-Path -LiteralPath $phoneLog) {
            $phonePattern = if ($Provider -eq 'cloudflare') { 'https://(?!api\.)[a-z0-9-]+\.trycloudflare\.com' } else { 'https://[a-z0-9-]{8,64}\.(?:lhr\.life|localhost\.run)' }
            $phoneOut = Join-Path $phoneRoot ('data\phone-tunnel-' + $phoneStamp + '-out.log')
            $phoneMatch = Select-String -LiteralPath @($phoneLog,$phoneOut) -Pattern $phonePattern -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($phoneMatch) {
                $phoneUrl = $phoneMatch.Matches[0].Value
                & $phonePython $phoneHelper origin $phoneUrl
                if ($LASTEXITCODE -ne 0) { throw 'Could not save phone origin' }
                $phoneVerified = $false
                for ($phoneProbe=0; $phoneProbe -lt 8; $phoneProbe++) {
                    & $phonePython $phoneHelper verify
                    if ($LASTEXITCODE -eq 0) { $phoneVerified = $true; break }
                    Start-Sleep -Seconds 2
                }
                if (-not $phoneVerified) { & $phonePython $phoneHelper disable; throw 'Phone URL could not be verified; pairing remains disabled' }
                Write-Output ('Phone URL: ' + $phoneUrl)
                Write-Output 'Open Hunter on the PC, press On phone, then Create code. Scan the QR with Android Chrome.'
                return
            }
        }
        if ($phoneTunnel.HasExited) { throw ('Tunnel stopped. Check ' + $phoneLog) }
        Start-Sleep -Seconds 1
    }
    throw ('Tunnel did not provide a URL. Check ' + $phoneLog)
} finally { Pop-Location }
