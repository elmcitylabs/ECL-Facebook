all: pyc version commit upload

init:
	python setup.py develop
	pip install -r requirements.txt

version:
	echo "Packaging version ${VERSION}"
	sed -i '' 's/\(__version__ = \).*/\1"${VERSION}"/g' ecl_facebook/__init__.py

commit:
	git add .
	git commit -m "bump version to ${VERSION}"

upload: version
	python setup.py sdist upload
	s3cmd put dist/ecl_facebook-${VERSION}.tar.gz s3://packages.elmcitylabs.com/ -P

pyc:
	find . -name "*.pyc" -exec rm '{}' ';'

