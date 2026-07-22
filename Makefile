.PHONY: setup play test validate check newcomer

setup:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

play:
	python dojo_classroom.py

test:
	python -m unittest discover -s tests

validate:
	python validate_missions.py

check: test validate

newcomer: setup check
	@echo "✅ Ready. Run 'make play' or 'python newcomer.py --play' to start the dojo."
