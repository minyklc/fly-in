all:
	
install:
	pip install -r requirements.txt

run:
	python3 main.py maps/challenger/01_the_impossible_dream.txt

debug:
	python3 -m pdb main.py maps/challenger/01_the_impossible_dream.txt

clean:
	rm -rf .mypy_cache __pycache__ venv .venv

lint:
	python3 -m flake8 . && python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 . && python3 -m mypy . --strict

.PHONY: all install run debug clean lint lint-strict