#!/bin/bash
source env/bin/activate
exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app