# build the LaiNES code, test the Python interface, and build
# the deployment package
all: test deployment

#
# MARK: Development
#

# run the Python test suite
test:
	python -m unittest discover .

#
# MARK: Deployment
#

# clean the build directory
clean:
	rm -rf build/ dist/ .eggs/ *.egg-info/ || true

# build the deployment package
deployment: clean
	python setup.py sdist bdist_wheel --universal

# ship the deployment package to PyPi
ship: deployment
	twine upload dist/*
