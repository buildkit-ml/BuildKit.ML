install:
	python setup.py install

format:
	autoflake -i **/*.py
	isort -i mlsphere/**/*.py
	yapf -i **/*.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf mlsphere.egg-info

build:
	python3 setup.py sdist bdist_wheel

test:
	PYTHONPATH=./ python3 tests/server.py

publish-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish:
	twine upload dist/*