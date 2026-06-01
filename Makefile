UV := uv


.PHONY: format


format:
	$(UV) format
	$(UV) tool run ty check
