.PHONY: setup run test clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run:
	@echo "Usage: .venv/bin/python utils.py input.pdf output.pdf --search PATTERN --action Highlight"

test:
	.venv/bin/python -m pytest tests/ -q

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
