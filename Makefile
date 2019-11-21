PRPM := pipenv run python test_project/manage.py

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

sdist: clean
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

env-prepare: ## install environment
	pipenv install --dev

.PHONY: .coverage
.coverage:
	coverage run --source=webmaster_verification quicktest.py webmaster_verification
	coverage run --source=webmaster_verification quicktest.py webmaster_verification --multicode

coverage: .coverage
	coverage html -d coverage

release: sdist ## package and upload a release
	twine upload dist/*

.PHONY: check-migrations
check-migrations: ## check that all migrations are created
	$(PRPM) makemigrations --check --dry-run

.PHONY: check
check: ## check
	$(PRPM) check