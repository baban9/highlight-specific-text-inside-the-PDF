.PHONY: setup test run build clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"

test:
	.venv/bin/python -m pytest tests/ -q

run:
	@echo "Example: .venv/bin/pdfmark annotate input.pdf output.pdf --search PATTERN --action Highlight"

build:
	.venv/bin/python -m build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist build src/*.egg-info .venv
