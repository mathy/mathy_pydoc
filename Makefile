.PHONY: docs test
venv:
	pip install virtualenv --upgrade
	virtualenv -p python3.7 env3.7
	env3.7/bin/pip install -r requirements.txt -r requirements-dev.txt

test: venv
	env3.7/bin/tox

publish: venv
	env3.7/bin/python setup.py sdist bdist_wheel
	env3.7/bin/twine upload dist/*
	rm -rf build dist .egg mathy_pydoc.egg-info

clean:
	rm -rf build dist .egg mathy_pydoc.egg-info env3.7

check: test
