#!/bin/bash
set -e

# Build and deploy python package
. .env/bin/activate
git config --global user.email "justin@dujardinconsulting.com"
git config --global user.name "justindujardin"
echo "Build and publish to pypi..."
rm -rf build dist
echo "--- Install requirements"
pip install twine wheel
echo "--- Buid dists"
python setup.py sdist bdist_wheel
echo "--- Upload to PyPi"
# NOTE: ignore errors on upload because our CI is dumb and tries to upload
#       even if the version has already been uploaded. This isn't great, but
#       works for now. Ideally the CI would not call this script unless the
#       semver changed.
set +e
twine upload -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD} dist/*
rm -rf build dist


# The build/deploy step runs in two commits. The first runs the tests and generates a
# tag commit, and that tag commit deploys to pypi. To make this work we do the pypi
# bit first, then run semantic-release to bump versions and generate a new commit. This
# way the package is always published from the tag commit, and not accidentally by the
# initiating change because the version was already bumped.
echo "Installing semantic-release requirements"
npm install 
echo "Updating build version"
npx ts-node tools/set-build-version.ts
echo "Running semantic-release"
npx semantic-release
