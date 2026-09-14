# Deployment Guide (DEPLOY.md)

For other languages (ja/zh), see `startup_messages.py` and application i18n.


Set before starting the application:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key (required; no default). |
| `DATABASE_URI` | Full DB URI, or use `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` instead. |
| `HOST` | Bind host (default `0.0.0.0`). |
| `PORT` | Bind port (default `5000`). |
| `FLASK_ENV` | `development` or `production`; only in development is `debug` enabled. |
| `RUN_DB_INIT` | Set to `true` to run DB init on startup (dev/first deploy only; use separate script in production). |
| `CORS_ORIGINS` | Comma-separated origins (default `*`; restrict in production). |

Optional: `CORS_METHODS`, `CORS_ALLOW_HEADERS`, `LANG`/`LC_ALL` for startup message locale.



```bash
export SECRET_KEY=your-secret-key
export DB_NAME=your_db
# optional: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD
python run.py
```


```bash
export SECRET_KEY=your-secret-key
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

Or use the generated script:

```bash
chmod +x run.sh
./run.sh
```


Build:

```bash
docker build -t app .
```

Run (pass env or use env file):

```bash
docker run -p 5000:5000 -e SECRET_KEY=xxx -e DB_NAME=xxx app
```


- **GET /health**: Liveness; returns 200 and `{"status":"ok","message":"..."}`. Use for liveness probes.
- **GET /ready**: Readiness; checks DB connectivity; returns 200 if OK, 503 if DB unreachable. Use for readiness probes.

Message field is i18n (ja/zh/en) via `startup_messages.py`.


The project can generate `celery_app.py` for background tasks. To run long-running work off the request path:

1. Install Redis and set `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` (e.g. `redis://localhost:6379/0`).
2. Start a worker: `celery -A celery_app worker -l info`.
3. In your Flask code, call tasks with `.delay()`: `from celery_app import example_task; example_task.delay(1, 2)`.

Add custom tasks to `celery_app.py` and register them in the `include` list if using autodiscovery.
