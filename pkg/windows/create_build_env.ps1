﻿# Script to install hubble dependencies and create executible

#Declaring Paramaters
Param(
  [bool]$default=$false,
  [string]$repo=$null,
  [string]$branch="develop"
)

$chocoVer = "0.10.5"
$gitVer = "2.12.0"
$portGitVer = "2.16.1.4"
# Verify you are running with elevated permission mode (administrator token)
if (!([bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544"))) {
    Write-Error "You must be running powershell with elevated permissions (run as administrator)"
    break
}

# Function to reload the environment
function reloadEnv() {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

#move to a better directory
if (!(Test-Path C:\temp)) {
    New-Item -Path C:\temp -ItemType Directory
}
set-location c:\temp

# Install\upgrade Chocolatey and Git if not present
if (!(Test-Path C:\ProgramData\chocolatey)) {
    Invoke-WebRequest https://chocolatey.org/install.ps1 -UseBasicParsing | Invoke-Expression
    reloadEnv
} else {
    $chocoCur = (choco)[0] -replace "Chocolatey v",""
    if ($chocoCur -lt $chocoVer) {
        choco upgrade chocolatey -y
    }
}

$git = choco list --localonly | Where-Object {$_ -like "git *"}
if (!($git)) {
    choco install git -y
    reloadEnv
} else {
    if (($git -replace "git ","") -lt $gitVer) {
        choco upgrade git -y
    }
}

$7zip = choco list --localonly | Where-Object {$_ -like "7zip*"} 
if (!($7zip)) {
    choco install 7zip -y
    reloadEnv
}

# Install salt and dependencies - including python
if (Test-Path .\salt) {
    Remove-Item -Recurse -Force salt
}
Push-Location
git clone https://github.com/saltstack/salt
Set-Location salt\pkg\windows
git checkout v2018.3.0
powershell -file build_env_2.ps1 -Silent
Pop-Location
Push-Location salt
reloadEnv
python -m pip install --upgrade pip
pip install -e .
Pop-Location

# Install hubble and dependency
if (Test-Path .\hubble) {
    Remove-Item -Recurse -Force hubble
}
#Checks to see if any paramaters were given for both $repo and $branch.
if ($default) {
    $repo = "https://github.com/hubblestack/hubble"
    $branch = "master"
}
#If no default was specified and no paramaters were given in the script, it prompts for a repo and branch
if ($repo -notlike "https*") {
    $repo = Read-Host "Enter a Repository (full URL only)"
    if (!($branch)) {
        $branch = Read-Host "Enter a Branch"
    }
}
Write-Error "---------------will be cloning1 : $repo"
Write-Error "---------------will be cloning2 : $branch"
git clone $repo
Push-Location hubble\pkg\windows
if ($branch -like "\W.+") {
    git checkout $branch
}
$lines = Get-Content pyinstaller-requirements.txt | Where-Object {$_ -notmatch '^\s+$'} 
foreach ($line in $lines) {
    $line = $line -replace "#.+$",""
    if ($line -notlike '*pyinotify*' -and $line -notlike '*salt-ssh*') { #pyinotify and salt-ssh are for linux only
        pip install $line
    }
}
Pop-Location

# Download PortableGit.  Requirement for Hubble
$port_git = choco list --localonly | Where-Object {$_ -like "git.portable *"}
if (!($port_git)) {
    choco install git.portable -y
    reloadEnv
} else {
    if (($port_git -replace "git.portable ","") -lt $portgitVer) {
        choco upgrade git.portable -y
    }
}
#Moves Portable Git into the correct location to work with hubble. 
set-location C:\Temp
Import-Module "$env:ChocolateyInstall\helpers\chocolateyInstaller.psm1" -Force;
$ChocoTools = Get-ToolsLocation

if ([string]::IsNullOrEmpty($ChocoTools)) {
    $ChocoTools = [System.Environment]::GetEnvironmentVariable("ChocolateyToolsLocation","User")
}

if(!(test-path .\hubble\PortableGit\)) {
    mkdir C:\Temp\hubble\PortableGit\
}

if (!(test-path "$ChocoTools\git\git-cmd.exe")) {
    choco install git.portable -y --force
}
Move-Item -Path $ChocoTools\git\ -Destination C:\Temp\hubble\PortableGit\ 

# Install osquery for executible
if (!(Test-path C:\ProgramData\osquery)) {
	choco install osquery -y
} else {
	choco upgrade osquery -y
}
reloadEnv

# Modify gitfs fix for incorrect path variables until fix has been upstreamed
if (!(Test-Path C:\Python27\Lib\site-packages\salt)) {
    Copy-Item .\salt\salt -Destination C:\Python27\Lib\site-packages\ -Recurse -Force
}

$gitfsFile = Get-Content C:\Python27\Lib\site-packages\salt\utils\gitfs.py
$gitfsFile = $gitfsFile -replace "files.add\(add_mountpoint\(relpath\(repo_path\)\)\)","files.add('/'.join(repo_path.partition('.:\\')[2].split(os.sep)))"
$gitfsFile | Set-Content C:\Python27\Lib\site-packages\salt\utils\gitfs.py -Force

#Remove obligitory c:\salt and c:\tools directory if it was created during script run
if (Test-Path C:\salt) {
    $empty = Get-ChildItem C:\salt
    if ($empty -eq $null) {
        Remove-Item C:\salt
    }
}

if (Test-Path C:\tools) {
    Remove-Item C:\tools -force
}
