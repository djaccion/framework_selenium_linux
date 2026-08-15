.PHONY: install test smoke report clean

install:
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

test:
	python3 -m pytest

smoke:
	python3 -m pytest -m smoke

report:
	python3 -m pytest --html=reportes/reporte.html --self-contained-html

clean:
	rm -rf .pytest_cache __pycache__ */__pycache__ evidencias reportes
