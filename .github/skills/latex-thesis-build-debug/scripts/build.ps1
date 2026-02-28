param(
  [Parameter(Mandatory = $false)]
  [string]$Entry = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Entry)) {
  if (Test-Path "main.tex") {
    $Entry = "main.tex"
  } elseif (Test-Path "初版/main.tex") {
    $Entry = "初版/main.tex"
  } else {
    $Entry = "main.tex"
  }
}

if (-not (Test-Path $Entry)) {
  throw "Entry file not found: $Entry"
}

# Requires TeX Live/MiKTeX with latexmk + xelatex.
latexmk -xelatex -interaction=nonstopmode -file-line-error $Entry
