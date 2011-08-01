#!/bin/bash

git add .
git cim "bump version to $1"
git archive --format=tar master > ecl_facebook-$1.tar
gzip -f ecl_facebook-$1.tar
s3cmd put ecl_facebook-$1.tar.gz s3://packages.elmcitylabs.com/ -P
