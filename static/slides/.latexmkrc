@default_files = ("main.tex");

$pdf_mode = 5;

$xelatex = "xelatex -shell-escape -file-line-error -halt-on-error -interaction=nonstopmode %O %S";

$aux_dir = '.cache';
$out_dir = '.cache';

$out2_dir = '.';
