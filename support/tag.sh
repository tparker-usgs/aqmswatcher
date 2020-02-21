#!/bin/sh

VERSION=`python3 -c "import aqmswatcher; print(aqmswatcher.__version__)"`
echo Tagging release $VERSION
git add aqmswatcher/__init__.py
git commit -m 'version bump'
git push \
&& git tag $VERSION \
&& git push --tags
