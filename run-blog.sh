#!/bin/sh
exec gunicorn -b localhost:8000 -w 4 cms:app

