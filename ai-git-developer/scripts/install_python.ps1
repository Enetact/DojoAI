# Ensure script is running as administrator
$admin = [System.Security.Principal.WindowsPrincipal] [System.Security.Principal.WindowsIdentity]::GetCurrent()
$adminRole = [System.Security.Principal.WindowsBuiltInRole]::Administrator
if (-Not $admin.IsInRole($adminRole)) {
    Write-Host " This script must be run as Administrator!"
    Start-Process powershell.exe -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

Write-Host " Installing Python and setting up environment variables..." -ForegroundColor Cyan

# Define Python installation variables
$pythonInstaller = "python-installer.exe"
$pythonDownloadURL = "https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe"
$pythonInstallPath = "C:\Python310"

# Download Python installer
Write-Host "⬇ Downloading Python 3.10.10..."
Invoke-WebRequest -Uri $pythonDownloadURL -OutFile $pythonInstaller

# Install Python silently
Write-Host " Installing Python..."
Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 TargetDir=$pythonInstallPath" -Wait

# Clean up installer
Remove-Item -Path $pythonInstaller -Force
Write-Host " Python installed successfully!" -ForegroundColor Green

# Add Python to system PATH manually
Write-Host " Adding Python to System PATH..."
$envPaths = [System.Environment]::GetEnvironmentVariable("Path", "Machine") -split ";"
$pythonPaths = @("$pythonInstallPath", "$pythonInstallPath\Scripts")
$updatedPaths = $envPaths + $pythonPaths | Select-Object -Unique
[System.Environment]::SetEnvironmentVariable("Path", ($updatedPaths -join ";"), "Machine")

# Restart Command Prompt for changes to apply
Write-Host " Restarting Command Prompt for changes to take effect..."
Start-Process -FilePath "cmd.exe" -ArgumentList "/c echo Python installed successfully. Please restart your system if needed." -NoNewWindow
Write-Host " Python installation complete! Run 'python --version' to verify." -ForegroundColor Green
