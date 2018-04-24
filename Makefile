
# build the deployment package
deployment:
	python3 setup.py sdist  
	python3 setup.py bdist_wheel

# ship the deployment package to PyPi
ship: deployment
	twine upload dist/*