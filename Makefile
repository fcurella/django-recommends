release:
	rm -rf dist
	rm -rf build
	rm -rf django_recommends.egg-info
	python setup.py sdist bdist_wheel
	twine upload dist/*
