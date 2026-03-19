param(
    [Parameter(Position = 0)]
    [string]$InputDir = "figures",

    [Parameter(Position = 1)]
    [string]$OutputDir = "figures",

    [string[]]$Files,

    [switch]$Recursive,

    [string]$Margins = "0"
)

$ErrorActionPreference = "Stop"

function Resolve-NormalizedPath([string]$Path) {
    return (Resolve-Path -LiteralPath $Path).Path
}

if (-not (Get-Command pdfcrop -ErrorAction SilentlyContinue)) {
    throw "pdfcrop not found in PATH. If you installed TeX Live, ensure its bin directory is on PATH (e.g. ...\\texlive\\2025\\bin\\windows)."
}

if (-not (Test-Path -LiteralPath $InputDir)) {
    throw "InputDir not found: $InputDir"
}

if (-not (Test-Path -LiteralPath $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

$inputRoot = Resolve-NormalizedPath $InputDir
$outputRoot = Resolve-NormalizedPath $OutputDir

$inputRootNorm = $inputRoot.TrimEnd('\\')
$outputRootNorm = $outputRoot.TrimEnd('\\')

$sourcePdfs = @()

if ($Files -and $Files.Count -gt 0) {
    foreach ($file in $Files) {
        $candidate = Join-Path $InputDir $file
        if (-not (Test-Path -LiteralPath $candidate)) {
            throw "File not found under InputDir: $candidate"
        }
        $sourcePdfs += (Resolve-NormalizedPath $candidate)
    }
} else {
    $searchParams = @{
        Path   = $InputDir
        Filter = "*.pdf"
        File   = $true
    }
    if ($Recursive) { $searchParams.Recurse = $true }

    $sourcePdfs = Get-ChildItem @searchParams | ForEach-Object { $_.FullName }
}

if (-not $sourcePdfs -or $sourcePdfs.Count -eq 0) {
    Write-Host "No PDF files found to crop." -ForegroundColor Yellow
    exit 0
}

Write-Host "Cropping PDFs from '$inputRoot' -> '$outputRoot' (margins=$Margins)" -ForegroundColor Cyan

foreach ($inFile in $sourcePdfs) {
    if (($inputRootNorm -ne $outputRootNorm) -and $inFile.StartsWith($outputRootNorm, [System.StringComparison]::OrdinalIgnoreCase)) {
        continue
    }

    $relative = $inFile.Substring($inputRoot.Length).TrimStart('\', '/')
    $outFile = Join-Path $outputRoot $relative
    $outDir = Split-Path -Parent $outFile

    if (-not (Test-Path -LiteralPath $outDir)) {
        New-Item -ItemType Directory -Path $outDir | Out-Null
    }

    Write-Host "- $relative" -ForegroundColor Gray

    # pdfcrop decides whether an input filename is "safe" using a strict regex.
    # On Windows, an absolute path contains backslashes (\), which fails that
    # check and makes pdfcrop try to create a symlink (often requires privileges).
    # Work around by copying the input to a workspace-local temp file and passing
    # pdfcrop a *relative* path that uses forward slashes.
    $tempDirAbs = Join-Path $PWD ".pdfcrop-temp"
    if (-not (Test-Path -LiteralPath $tempDirAbs)) {
        New-Item -ItemType Directory -Path $tempDirAbs | Out-Null
    }

    $tempName = "pdfcrop_in_" + [guid]::NewGuid().ToString("N") + ".pdf"
    $tempInAbs = Join-Path $tempDirAbs $tempName
    Copy-Item -LiteralPath $inFile -Destination $tempInAbs -Force

    # Relative path (forward slashes) so pdfcrop treats it as safe.
    $tempInRel = "./.pdfcrop-temp/$tempName"

    try {
        & pdfcrop --margins $Margins --clip $tempInRel $outFile | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "pdfcrop failed ($LASTEXITCODE) for: $relative"
        }
    }
    finally {
        Remove-Item -LiteralPath $tempInAbs -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Done." -ForegroundColor Green
