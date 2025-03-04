#!/usr/bin/env sh
##
# Install current extension.
#
set -e

if [ "$VENV_DIR" != "" ]; then
  . ${VENV_DIR}/bin/activate
fi
pip install -r "dev-requirements.txt"
pip install -r "requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-archiver/requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-dcat/requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-qa/requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-qgov/requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-scheming/requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-validation/requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-xloader/requirements.txt"
pip install -r "$VENV_DIR/src/ckanext-ytp-comments/requirements.txt"
python setup.py develop
installed_name=$(grep '^\s*name=' setup.py |sed "s|[^']*'\([-a-zA-Z0-9]*\)'.*|\1|")

# Validate that the extension was installed correctly.
if ! pip list | grep "$installed_name" > /dev/null; then echo "Unable to find the extension in the list"; exit 1; fi

if [ "$VENV_DIR" != "" ]; then
  deactivate
fi
