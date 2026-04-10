$pdf_mode = 1;
$pdflatex = 'bash tools/auto-crop-pdfs.sh && xelatex -interaction=nonstopmode -synctex=1 %O %S';
$bibtex = 'biber %O %B';
