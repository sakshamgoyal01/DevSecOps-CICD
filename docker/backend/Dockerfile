# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- Workdir ----------
WORKDIR /app

# ---------- System dependencies ----------
RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# ---------- Copy requirements first (better caching) ----------
COPY src/backend/requirements.txt ./requirements.txt

# ---------- Install Python dependencies ----------
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy backend source code ----------
COPY src/backend/ .

# ---------- Expose Flask/Gunicorn port ----------
EXPOSE 5001

# ---------- Start app with Gunicorn ----------
CMD ["python", "app.py"]