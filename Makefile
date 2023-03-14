help:
	@echo "build - Build package"
	@echo "install - Install package to local system"
	@echo "clean - Clean built artifacts"

build:
	python setup.py build sdist
	cp dist/* packer/build/

install:
	pip install .
	python setup.py clean

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name __pycache__ -delete
	rm -rf ./build ./dist ./*.egg-info


