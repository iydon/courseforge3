UV := uv


.PHONY: format sync


format:
	$(UV) format
	$(UV) tool run ty check

sync:
	$(UV) sync --all-packages
