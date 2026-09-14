# py_dockerfile.vm - generated Dockerfile for Flask app (multi-stage, non-root)
# Build stage: install deps
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Run stage: copy app and run as non-root
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
# Copy application
COPY . .
# Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 5000
# Production: use gunicorn. Override CMD for different bind (e.g. 0.0.0.0:5000)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
