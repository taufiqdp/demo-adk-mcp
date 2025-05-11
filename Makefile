format:
	uv run black . && uv run isort . 

lint:
	uv run ruff check

check: format lint