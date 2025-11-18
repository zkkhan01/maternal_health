FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Note: In production start Pathway separately or run a process manager to run both services.
CMD ["uvicorn", "app.server.api:app", "--host", "0.0.0.0", "--port", "8000"]
