fmt:
	isort .
	black .

lint:
	isort . --check-only
	black . --check
	mypy cf_pipelines/

test:
	pytest --cov=cf_pipelines --cov-report html -v tests/

release-major:
	bumpversion --config-file version.cfg --verbose major

release-minor:
	bumpversion --config-file version.cfg --verbose minor

release-patch:
	bumpversion --config-file version.cfg --verbose patch

build-quiet:
	@poetry build -q && echo "$(shell poetry version -s)"

