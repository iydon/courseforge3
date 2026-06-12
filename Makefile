UV := uv


.PHONY: build format sync


format:
	$(UV) format
	$(UV) tool run ty check

build:
	$(UV) build

sync:
	$(UV) sync --all-packages
