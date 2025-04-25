#!/bin/bash

# create virtual enviroment
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# setup .flask_env file
python -c 'import secrets; print(f"SECRET_KEY={secrets.token_hex()}")' > .flask_env

# create static directory for images
mkdir ./static
