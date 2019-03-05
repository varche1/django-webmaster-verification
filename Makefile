test: clean-pyc clean
	pipenv run python quicktest.py webmaster_verification
	pipenv run python quicktest.py webmaster_verification --multicode

test-travis:
	python quicktest.py webmaster_verification
	python quicktest.py webmaster_verification --multicode

install:
	pipenv run python setup.py install

build:
	pipenv run python setup.py build

sdist:
	pipenv run python setup.py sdist

upload:
	pipenv run python setup.py sdist upload

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean:
	rm -rf dist build *.egg-info django-webmaster-verification-*
	rm -rf .coverage coverage

clean-venv: ## remove local venv
	rm -rf `pipenv --venv`

.PHONY: .coverage
.coverage:
	coverage run --source=webmaster_verification quicktest.py webmaster_verification
	coverage run --source=webmaster_verification quicktest.py webmaster_verification --multicode

coverage: .coverage
	coverage html -d coverage
