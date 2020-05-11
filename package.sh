#!/bin/bash
VERSION=$(cat setup.py | grep version | cut -d '=' -f 2 | cut -d '"' -f 2)
echo "Packaging and uploading package version $VERSION"
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*$VERSION* --verbose
