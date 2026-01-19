run:
	streamlit run app/main.py

venv:
	python -m venv .venv

install:
	pip install -r requirements.txt

test:
	python -m pytest -q
