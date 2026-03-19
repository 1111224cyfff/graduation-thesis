# Skill: Auto-crop LaTeX figures (remove whitespace)

## What it does
- Crops extra margins from figure PDFs.
- By default, overwrites the original PDFs in `figures/`.

## Use it when
- A figure looks too small even with large `width=...`.
- The exported PDF page has big blank borders.

## Default policy (repo convention)
- Figures referenced in the thesis should be cropped by default to remove excessive whitespace.
- For PDF figures under `figures/`, run the crop script after adding/replacing PDFs. Use a small padding (e.g. `-Margins '2'`) to avoid cutting thin lines or annotations.
- For PNG/JPG that contain visible borders, trim whitespace before referencing them in LaTeX.

## Commands (from repo root)
- Crop specific PDFs:
  - `powershell -ExecutionPolicy Bypass -Command ".\tools\crop-figures.ps1 -Files 'a.pdf','b.pdf' -Margins '2'"`
- Crop all PDFs in `figures/`:
  - `powershell -ExecutionPolicy Bypass -File tools/crop-figures.ps1 -Margins '2'`
- Add padding (points):
  - `powershell -ExecutionPolicy Bypass -Command ".\tools\crop-figures.ps1 -Files 'a.pdf' -Margins '5'"`

## Automated Workflow for Figure Insertion

### How it works
1. **White Margin Detection**:
   - For PDF figures: Uses `pdfcrop` to check for excessive margins.
   - For PNG/JPG figures: Uses ImageMagick's `-trim` to detect whitespace.

2. **Auto-cropping**:
   - If white margins are detected, the `crop-figures.ps1` script is automatically invoked.
   - Default margin padding is set to `2` points to avoid cutting annotations.

3. **Integration with LaTeX**:
   - When inserting a figure, the workflow ensures the cropped version is used.
   - Updates LaTeX references to point to the processed figure.

### Example Workflow
- Insert a figure:
  ```latex
  \includegraphics[width=0.8\textwidth]{figures/example.pdf}
  ```
- The system will:
  1. Check if `figures/example.pdf` has white margins.
  2. If margins exist, crop the figure using:
     ```powershell
     powershell -ExecutionPolicy Bypass -Command ".\tools\crop-figures.ps1 -Files 'figures/example.pdf' -Margins '2'"
     ```
  3. Replace the original figure with the cropped version.

### Notes
- Ensure `pdfcrop` and ImageMagick are installed and available in the system `PATH`.
- This workflow is triggered automatically during figure insertion or manual invocation of the crop script.

## Notes
- `pdfcrop` is provided by TeX Live. If `pdfcrop` is not found, add TeX Live `bin\windows` to `PATH`.
- For PNG/JPG, use ImageMagick if available: `magick in.png -trim +repage out.png`.
