.PHONY: x fmt lint fix

x: fmt

fmt:
	uv run ruff format .

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix .
