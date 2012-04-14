all: pyc version commit upload

init:
	python setup.py develop
	pip install -r requirements.txt

version:
	echo "Packaging version ${MAJ}.${MIN}"
	sed -i '' 's/\(__version__ = \).*/\1"${MAJ}.${MIN}"/g' ecl_facebook/metadata.py
	sed -i '' 's/\(version = \).*/\1"${MAJ}"/g' ecl_facebook/metadata.py
	sed -i '' 's/\(release = \).*/\1"${MIN}"/g' ecl_facebook/metadata.py

commit:
	git add .
	git commit -m "bump version to ${VERSION}"

upload: version
	python setup.py sdist upload
	s3cmd put dist/ecl_facebook-${VERSION}.tar.gz s3://packages.elmcitylabs.com/ -P

pyc:
	find . -name "*.pyc" -exec rm '{}' ';'

documentation:
	cd docs && make html

push:
	git push github master
	git push origin master
	cd docs && make html && cd _build/html && git add . && git commit -m "doc update" && git push

