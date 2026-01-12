#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run collectstatic
# This puts all static files in the folder defined in your STATIC_ROOT
python3.9 manage.py collectstatic --noinput