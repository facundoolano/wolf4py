.PHONY: venv run

deps:
	python3 -m venv venv &&	. venv/bin/activate &&\
	pip install -r requirements.txt

run: data/VGAHEAD.WL6
	. venv/bin/activate && python wolf/main.py
