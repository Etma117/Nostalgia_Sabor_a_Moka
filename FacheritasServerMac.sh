#!/bin/bash

source ToolCraftEnv/bin/activate

python -c "import sys; print(sys.executable)"

pip install -r requirements.txt >/dev/null 2>&1

python manage.py runserver >/dev/null 2>&1 &

sleep 5

open http://127.0.0.1:8000
