
#!/bin/sh
# py_run_script.vm - generated run.sh for production/development
# Set env vars as needed (override for production)
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-5000}"
export FLASK_ENV="${FLASK_ENV:-production}"
# Optional: activate venv if present
if [ -d "venv" ]; then
  . venv/bin/activate
fi
# Production: gunicorn; development: use python run.py
if [ "$FLASK_ENV" = "development" ]; then
  exec python run.py
else
  exec gunicorn -w 4 -b "${HOST}:${PORT}" run:app
fi

