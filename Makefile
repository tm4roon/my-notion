.PHONY: x fmt lint fix

x: fix fmt

fmt:
	uv run ruff format .

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix .
