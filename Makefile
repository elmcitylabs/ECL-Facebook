all: pyc version

init:
	virtualenv .
	. bin/activate && python setup.py develop

pyc:
	find . -name "*.pyc" -exec rm '{}' ';'

version: pyc
	echo "Packaging version ${MAJ}.${MIN}"
	sed -i '' 's/\(__version__ = \).*/\1"${MAJ}.${MIN}"/g' ecl_facebook/metadata.py
	sed -i '' 's/\(version = \).*/\1"${MAJ}"/g' docs/conf.py
	sed -i '' 's/\(release = \).*/\1"${MAJ}.${MIN}"/g' docs/conf.py
	git add ecl_facebook/metadata.py
	git add docs/conf.py
	git commit -m "bump version to ${MAJ}.${MIN}"
	python setup.py sdist upload
	s3cmd put dist/ecl_facebook-${VERSION}.tar.gz s3://packages.elmcitylabs.com/ -P

documentation:
	cd docs && make html

push: documentation
	git push github master
	git push origin master
	cd docs/_build/html && git add . && git commit -m "doc update" && git push

