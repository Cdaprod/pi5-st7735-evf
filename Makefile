SHELL := /bin/bash
PYTHON ?= python3
VENV ?= .venv

.PHONY: install test test-display run probe lint zip clean

test:
	python -m unittest discover -s tests -v

install:
	sudo ./scripts/install_pi.sh

test-display:
	source $(VENV)/bin/activate && python tools/display_test.py

run:
	source $(VENV)/bin/activate && python evf.py

probe:
	./tools/probe_capture.sh

lint:
	source $(VENV)/bin/activate && python -m compileall evf.py pi5_st7735_evf tools/display_test.py

zip:
	cd .. && zip -r pi5-st7735-evf.zip pi5-st7735-evf -x "*/.venv/*" "*/vendor/Python_ST7735/*" "*/__pycache__/*"

clean:
	rm -rf __pycache__ pi5_st7735_evf/__pycache__ tools/__pycache__
