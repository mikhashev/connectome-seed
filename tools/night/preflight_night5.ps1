<#
preflight_night5.ps1 -- everything that must be true BEFORE night 5 starts, checked now
rather than remembered.

Why this file exists. The night-5 brief's §5 lists void conditions, and every gate in §4
fires *after* the night: gate 7 compares configs once a run json exists, gate 8 compares
the environment, gate 4 catches contention only after two four-hour runs. The one
confounder that has actually recurred -- another process resident on the GPU -- is caught
by none of them in advance. It was stopped once on 2026-09-17 and was back on 2026-09-18
under a new PID, holding 27.8 GiB. So the class is "recurring", not "one-off", and the
answer to a recurring confounder is a check that runs every time, not a line someone is
supposed to recall.

Everything here refuses loudly with the measured value beside the expected one. Nothing
here starts anything.

Usage:
    powershell -ExecutionPolicy Bypass -File tools\night\preflight_night5.ps1

Exit codes:
    0  every check passed; the night may be launched
    1  at least one check REFUSED -- the launch would be void or would fail
    2  checks passed but at least one WARNING needs a human decision

Windows PowerShell 5.1 compatible (no &&, no ternary, no null-coalescing).
#>
[CmdletBinding()]
param(
    [string]$Repo = "C:\Users\mikha\Documents\dpc-research\connectome-seed",
    [string]$DataRoot = "C:\Users\mikha\Documents\dpc-research\connectome-seed-data",
    [string]$Ensemble = "9992",
    [string]$Tag = "night5"
)

$script:Refusals = @()
$script:Warnings = @()

function Say-Pass([string]$name, [string]$detail) {
    Write-Output ("  PASS    " + $name.PadRight(34) + $detail)
}
function Say-Refuse([string]$name, [string]$detail) {
    Write-Output ("  REFUSE  " + $name.PadRight(34) + $detail)
    $script:Refusals += ($name + " -- " + $detail)
}
function Say-Warn([string]$name, [string]$detail) {
    Write-Output ("  WARN    " + $name.PadRight(34) + $detail)
    $script:Warnings += ($name + " -- " + $detail)
}

Write-Output "=============================================================================="
Write-Output ("night 5 pre-flight -- " + (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ") + " UTC")
Write-Output ("repo " + $Repo)
Write-Output "=============================================================================="

# ---------------------------------------------------------------- 1. the card is free
# Nights 1-4 each recorded total GPU memory in use at the end of the run between 3,720 and
# 4,805 MiB -- that is the whole card, desktop included. So a card that is free in the
# sense those nights were free reads well under 6 GiB before anything starts, and gate 4's
# timing bands were measured in exactly that state.
Write-Output ""
Write-Output "1. the GPU"
$smi = & nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($smi)) {
    Say-Refuse "nvidia-smi" "did not answer; the card's state is unknown"
} else {
    $parts = $smi -split ","
    $used = [int]($parts[0].Trim())
    $total = [int]($parts[1].Trim())
    $detail = "used $used MiB of $total (nights 1-4 ran with 3720-4805 total)"
    if ($used -gt 6000) {
        Say-Refuse "GPU memory in use" ($detail + " -- something else is resident")
    } else {
        Say-Pass "GPU memory in use" $detail
    }
    $apps = & nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader 2>$null
    $heavy = @()
    foreach ($line in $apps) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($line -match "llama|python|ollama|vllm|torch|train") { $heavy += $line.Trim() }
    }
    if ($heavy.Count -gt 0) {
        Say-Refuse "compute processes on the card" ("resident: " + ($heavy -join " | "))
    } else {
        Say-Pass "compute processes on the card" "none of the known heavy kinds"
    }
}

# ------------------------------------------------- 2. the two network dirs must be free
# run_individual.py:375 refuses (exit 2, "nothing deleted") when the network dir exists.
# It refuses per run, so a collision on the SECOND job kills only that job -- after the
# first has already spent four hours.
Write-Output ""
Write-Output "2. the output coordinates"
foreach ($id in @("000", "003")) {
    $dir = Join-Path $DataRoot ("results\flow\" + $Ensemble + "\" + $id)
    if (Test-Path $dir) {
        Say-Refuse ("network dir " + $Ensemble + "/" + $id) ("already exists: " + $dir)
    } else {
        Say-Pass ("network dir " + $Ensemble + "/" + $id) "absent, as it must be"
    }
}
$nightDir = Join-Path $Repo "tools\night"
$leftovers = Get-ChildItem -Path $nightDir -Filter ("wave_" + $Tag + ".*") -ErrorAction SilentlyContinue
if ($leftovers) {
    Say-Warn "wave files from a previous try" (($leftovers | ForEach-Object { $_.Name }) -join ", ")
} else {
    Say-Pass "wave files for this tag" "none present"
}

# ------------------------------------------------------------ 3. the environment answers
Write-Output ""
Write-Output "3. the environment"
$py = Join-Path $Repo "tools\.venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Say-Refuse "venv interpreter" ("missing: " + $py)
} else {
    $probe = & $py -c "import sys, torch, flyvis; print(sys.version.split()[0], torch.__version__, torch.cuda.is_available(), flyvis.__version__)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Say-Refuse "venv imports" ("failed: " + ($probe -join " "))
    } elseif ($probe -notmatch "True") {
        Say-Refuse "CUDA availability" ("torch reports: " + $probe)
    } else {
        Say-Pass "venv answers" $probe
    }
}

# -------------------------------------------------------------- 4. provenance of the run
Write-Output ""
Write-Output "4. provenance"
Push-Location $Repo
$dirty = & git status --porcelain
if (-not [string]::IsNullOrWhiteSpace(($dirty -join ""))) {
    Say-Warn "working tree" "not clean; the night's provenance will name a dirty tree"
} else {
    Say-Pass "working tree" "clean"
}
$ahead = & git rev-list --count "origin/master..HEAD" 2>$null
if ($LASTEXITCODE -eq 0) {
    if ([int]$ahead -gt 0) {
        Say-Warn "unpushed commits" ($ahead + " ahead of origin/master")
    } else {
        Say-Pass "unpushed commits" "none; HEAD is on origin"
    }
}
$head = & git log --format="%h %s" -1
Say-Pass "HEAD" $head
Pop-Location

# --------------------------------------------------------------------- 5. room on disk
Write-Output ""
Write-Output "5. disk"
$drive = Get-PSDrive -Name ($Repo.Substring(0,1))
$freeGiB = [math]::Round($drive.Free / 1GB, 1)
if ($freeGiB -lt 20) {
    Say-Refuse "free space" ("$freeGiB GiB -- a night writes run jsons and checkpoints")
} else {
    Say-Pass "free space" "$freeGiB GiB"
}

# ------------------------------------------------- 6. the machine staying up all night
# A Windows Update restart killed a run on 2026-09-14 at 23:31 UTC; that run is not in the
# substrate at all. Active hours are the only lever, and they are read here rather than
# assumed.
Write-Output ""
Write-Output "6. the machine staying up"
$uxKey = "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings"
try {
    $ux = Get-ItemProperty -Path $uxKey -ErrorAction Stop
    $start = $ux.ActiveHoursStart
    $end = $ux.ActiveHoursEnd
    if ($null -eq $start -or $null -eq $end) {
        Say-Warn "active hours" "not set in the registry; a restart may land inside the night"
    } else {
        # Windows defers an update restart ONLY inside active hours. The night runs roughly
        # 18:00 to 08:00 local, so the question is not "are active hours set" but "do they
        # cover the night". A window of 08:00-17:00 leaves the entire night unprotected --
        # which is exactly the state in which a restart killed a run at 23:31 UTC on
        # 2026-09-14, a run that is not in the substrate at all.
        $covers = $false
        if ([int]$start -gt [int]$end) {
            # a window that wraps midnight, e.g. 18 -> 8
            if ([int]$start -le 18 -and [int]$end -ge 8) { $covers = $true }
        }
        if ($covers) {
            Say-Pass "active hours (local)" ("$start`:00 to $end`:00 -- wraps midnight and covers the night window")
        } else {
            Say-Warn "active hours DO NOT cover the night" ("set to $start`:00-$end`:00 local; restarts are deferred only in THAT window, so 18:00-08:00 is unprotected. This is the state in which the 2026-09-14 23:31 restart killed a run. Windows allows an 18-hour span: 17:00-08:00 would cover the night.")
        }
    }
} catch {
    Say-Warn "active hours" "could not read the registry key"
}
$pending = $false
foreach ($k in @("HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired",
                 "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending")) {
    if (Test-Path $k) { $pending = $true }
}
if ($pending) {
    Say-Refuse "reboot pending" "Windows has a restart queued; it will land inside the night"
} else {
    Say-Pass "reboot pending" "no restart queued"
}

# ----------------------------------------------------------------- 7. the command itself
Write-Output ""
Write-Output "7. the launch command, dry-run now"
Push-Location $Repo
$dry = & powershell -ExecutionPolicy Bypass -File (Join-Path $Repo "tools\night\start_night.ps1") -DryRun -Tag $Tag -Ensemble $Ensemble -Seeds "0,3" -NoReplicate 2>&1
Pop-Location
$dryText = ($dry | Out-String)
$wantFirst = "--seed 0 --id " + $Ensemble + "/000"
$wantSecond = "--seed 3 --id " + $Ensemble + "/003"
if ($dryText -match [regex]::Escape($wantFirst) -and $dryText -match [regex]::Escape($wantSecond) -and $dryText -match "\[dry\] 2 commands") {
    $iFirst = $dryText.IndexOf($wantFirst)
    $iSecond = $dryText.IndexOf($wantSecond)
    if ($iFirst -lt $iSecond) {
        Say-Pass "dry run" "two jobs, seed 0 at $Ensemble/000 FIRST, seed 3 at $Ensemble/003 second"
    } else {
        Say-Refuse "dry run order" "seed 3 comes before seed 0; the brief puts 0-double-prime first"
    }
} else {
    Say-Refuse "dry run" "did not produce the two expected jobs"
}

# ------------------------------------------------------------------------ the summary
Write-Output ""
Write-Output "=============================================================================="
if ($script:Refusals.Count -gt 0) {
    Write-Output ("REFUSED -- " + $script:Refusals.Count + " check(s) say the night must not start:")
    foreach ($r in $script:Refusals) { Write-Output ("  - " + $r) }
    if ($script:Warnings.Count -gt 0) {
        Write-Output ("and " + $script:Warnings.Count + " warning(s):")
        foreach ($w in $script:Warnings) { Write-Output ("  - " + $w) }
    }
    Write-Output "=============================================================================="
    exit 1
}
if ($script:Warnings.Count -gt 0) {
    Write-Output ("PASSED with " + $script:Warnings.Count + " warning(s) needing a human decision:")
    foreach ($w in $script:Warnings) { Write-Output ("  - " + $w) }
    Write-Output "=============================================================================="
    exit 2
}
Write-Output "ALL CHECKS PASSED -- the night may be launched."
Write-Output "=============================================================================="
exit 0
