FONTS := $iroot/font/
TYPST := typst


main.pdf: main.typ section.typ
	$$(TYPST) compile --font-path $$(FONTS) main.typ $$@
