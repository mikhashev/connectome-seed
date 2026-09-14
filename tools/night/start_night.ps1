<#
start_night.ps1 -- start the overnight flyvis wave DETACHED and follow its progress log in this window.

  Closing this window (or Ctrl+C) stops only the follower; the runs continue.
  To stop the runs:   taskkill /T /F /PID (Get-Content <night>\wave_<tag>.pid)
  To re-attach later: start_night.ps1 -FollowOnly [-Tag <tag>]

Parameters
  -DryRun          print the launcher command and the launcher's own --dry listing; start nothing
  -FollowOnly      do not launch; only follow an existing wave_<tag>.progress.log
  -Tag / -Ensemble / -Seeds / -NIters / -Rungs / -ProgressEvery   launcher overrides (defaults = the night run)
  -Seeds "0,1,2,3,4,5"  comma list and/or ranges ("0-5"); the replicate 0' (id <ENS>/900) runs right after seed 0
                   unless -NoReplicate is given
  -NoReplicate     omit --replicate from the launcher args: no run 0' (id <ENS>/900) is queued
  -Extent N        flyvis hexagonal extent (default 15 = the flyvis default). When not 15 BOTH Hydra overrides are
                   passed: network.connectome.extent=N (config/network/connectome/connectome.yaml) and
                   task.dataset.boxfilter.extent=N (config/task/task.yaml) -- the task rendering does not
                   follow the network extent by itself
  -FollowSeconds N stop following after N seconds (0 = follow until WAVE DONE / Ctrl+C / window closed)

Windows PowerShell 5.1 compatible (no &&, no ??, no ternary).
#>
[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$FollowOnly,
    [switch]$NoReplicate,
    [string]$Tag = "night1",
    [string]$Ensemble = "9991",
    [string]$Seeds = "0",
    [int]$NIters = 250000,
    [string]$Rungs = "1000,5000,25000,250000",
    [int]$ProgressEvery = 100,
    [int]$Extent = 15,
    [int]$FollowSeconds = 0
)

$ErrorActionPreference = "Stop"

# ---- paths, relative to this script ----
$night    = $PSScriptRoot
$probe    = Split-Path -Parent $night
$py       = Join-Path $probe ".venv\Scripts\python.exe"
$launcher = Join-Path $night "launch_wave.py"

$env:FLYVIS_ROOT_DIR = "C:/Users/mikha/Documents/dpc-research/connectome-seed-data"

$pidFile     = Join-Path $night ("wave_" + $Tag + ".pid")
$progressLog = Join-Path $night ("wave_" + $Tag + ".progress.log")
$launcherLog = Join-Path $night ("wave_" + $Tag + ".launcher.log")
$waveJson    = Join-Path $night ("wave_" + $Tag + ".json")

if (-not (Test-Path $py))       { throw "venv python not found: $py" }
if (-not (Test-Path $launcher)) { throw "launcher not found: $launcher" }

# ---- the launcher command (sequential, detached, determinism OFF) ----
$launchArgs = @(
    $launcher,
    "--tag", $Tag,
    "--ensemble", $Ensemble,
    "--seeds", $Seeds,
    "--n-iters", "$NIters",
    "--rungs", $Rungs,
    "--progress-every", "$ProgressEvery",
    "--sequential", "--detach", "--no-determinism"
)
if (-not $NoReplicate) {
    $launchArgs += "--replicate"
}
if ($Extent -ne 15) {
    # both keys are required: the connectome extent and the task's boxfilter (rendering) extent are set separately
    $launchArgs += @("--override", ("network.connectome.extent=" + $Extent),
                     "--override", ("task.dataset.boxfilter.extent=" + $Extent))
}
$quoted = @()
foreach ($x in @($py) + $launchArgs) {
    if ($x -match '\s') { $quoted += ('"' + $x + '"') } else { $quoted += $x }
}
$cmdLine = $quoted -join ' '

Write-Output ("FLYVIS_ROOT_DIR = " + $env:FLYVIS_ROOT_DIR)
if ($Extent -eq 15) {
    Write-Output ("extent          : 15 (flyvis default, no override)")
} else {
    Write-Output ("extent          : " + $Extent + "  (overrides network.connectome.extent=" + $Extent + " task.dataset.boxfilter.extent=" + $Extent + ")")
}
if ($NoReplicate) {
    Write-Output ("seeds           : " + $Seeds + " (no replicate)")
} else {
    Write-Output ("seeds           : " + $Seeds + " + replicate 0' (id " + $Ensemble + "/900, runs right after seed 0)")
}
Write-Output ("PID file        : " + $pidFile)
Write-Output ("wave progress   : " + $progressLog + "   (START/EXIT + iter/RUNG/CHECKPOINT/DONE of the running job)")
Write-Output ("launcher log    : " + $launcherLog)
Write-Output ("wave record     : " + $waveJson)
Write-Output ("per-run files   : " + $night + "\<tag>_<ENS>-<NNN>.json / .log / .stdout.log")
Write-Output ("Closing this window does not stop the runs; to stop them: taskkill /T /F /PID (Get-Content '" + $pidFile + "')")
Write-Output ("Re-attach later : powershell -ExecutionPolicy Bypass -File '" + $PSCommandPath + "' -FollowOnly -Tag " + $Tag)
Write-Output ""
Write-Output ("command: " + $cmdLine)
Write-Output ""

if ($DryRun) {
    Write-Output "[DryRun] launcher --dry output follows; nothing is started:"
    & $py ($launchArgs + @("--dry"))
    exit $LASTEXITCODE
}

if (-not $FollowOnly) {
    # refuse a double launch of the same tag while its detached launcher is still alive
    if (Test-Path $pidFile) {
        $oldPid = (Get-Content -Path $pidFile | Select-Object -First 1).Trim()
        $old = $null
        if ($oldPid -match '^\d+$') {
            $old = Get-CimInstance Win32_Process -Filter ("ProcessId = " + $oldPid) -ErrorAction SilentlyContinue
        }
        if ($old -ne $null -and $old.CommandLine -like "*launch_wave.py*") {
            throw ("a launcher for tag '" + $Tag + "' is still running (PID " + $oldPid + "): " + $old.CommandLine +
                   " -- use -FollowOnly to watch it, or stop it first")
        }
    }
    & $py $launchArgs
    if ($LASTEXITCODE -ne 0) { throw ("launcher returned exit code " + $LASTEXITCODE) }
    if (-not (Test-Path $pidFile)) { throw ("launcher returned 0 but wrote no PID file: " + $pidFile) }
    Write-Output ("detached launcher PID " + (Get-Content -Path $pidFile) + " (from " + $pidFile + ")")
}

# ---- follow the wave progress log ----
$waitUntil = (Get-Date).AddSeconds(120)
while (-not (Test-Path $progressLog) -and (Get-Date) -lt $waitUntil) { Start-Sleep -Milliseconds 500 }
if (-not (Test-Path $progressLog)) {
    throw ("progress log did not appear within 120 s: " + $progressLog + " -- see " + $launcherLog)
}
Write-Output ("---- following " + $progressLog + " (Ctrl+C / closing the window stops only this view) ----")

if ($FollowSeconds -le 0) {
    # follow forever; leave the pipeline when the launcher writes its WAVE DONE line
    try {
        Get-Content -Path $progressLog -Wait -Tail 20 | ForEach-Object {
            Write-Output $_
            if ($_ -match ' WAVE DONE ') { throw "WAVE_DONE" }
        }
    } catch {
        if ($_.Exception.Message -ne "WAVE_DONE") { throw }
    }
} else {
    # timed follow: poll the file once a second until the deadline or WAVE DONE
    $deadline = (Get-Date).AddSeconds($FollowSeconds)
    $lines = @(Get-Content -Path $progressLog)
    $shown = [Math]::Max(0, $lines.Count - 20)
    $done = $false
    while (-not $done -and (Get-Date) -lt $deadline) {
        $lines = @(Get-Content -Path $progressLog)
        for ($i = $shown; $i -lt $lines.Count; $i++) {
            Write-Output $lines[$i]
            if ($lines[$i] -match ' WAVE DONE ') { $done = $true }
        }
        $shown = $lines.Count
        if (-not $done) { Start-Sleep -Seconds 1 }
    }
    if (-not $done) {
        Write-Output ("---- follow window of " + $FollowSeconds + " s elapsed; the runs continue (re-attach with -FollowOnly) ----")
    }
}
Write-Output "---- follower finished; the detached runs are independent of this window ----"
