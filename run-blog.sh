#!/bin/bash
# activate virtual environment
source venv/bin/activate
# start Waitress server
exec waitress-serve --port=8000 --threads=8 cms:app
# alternate example with Gunicorn server
# exec gunicorn -b localhost:8000 -w 4 cms:app

