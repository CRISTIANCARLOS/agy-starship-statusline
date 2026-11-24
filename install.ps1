# Installer script for Windows PowerShell
$ErrorActionPreference = "Stop"

$targetDir = Join-Path $HOME ".gemini\antigravity-cli"
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

$scriptUrl = "https://raw.githubusercontent.com/CRISTIANCARLOS/agy-starship-statusline/main/statusline.py"
$destScript = Join-Path $targetDir "statusline.py"

Write-Host "Downloading statusline.py..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $scriptUrl -OutFile $destScript

$settingsFile = Join-Path $targetDir "settings.json"
$settings = @{}
if (Test-Path $settingsFile) {
    try {
        $settings = Get-Content $settingsFile -Raw | ConvertFrom-Json -AsHashtable
    } catch {
        $settings = @{}
    }
}

$escapedPath = $destScript.Replace("\", "\\")
$settings["statusLine"] = @{
    "type" = "command"
    "command" = "python $escapedPath"
}

$settings | ConvertTo-Json -Depth 10 | Set-Content $settingsFile -Encoding UTF8

Write-Host "agy-starship-statusline installed successfully!" -ForegroundColor Green
Write-Host "Configured in: $settingsFile" -ForegroundColor Yellow
