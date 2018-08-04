init:
	pip install pipenv
	pipenv install --dev

flake:
	pipenv run flake8 graphist

lint:
	pipenv run pylint graphist