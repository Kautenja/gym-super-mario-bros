
# build the deployment package
deployment:
	python3 setup.py sdist  
	python3 setup.py bdist_wheel

# ship the deployment package to PyPi
ship:
	python3 setup.py sdist bdist_wheel upload