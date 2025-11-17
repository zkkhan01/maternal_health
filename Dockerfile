FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8020
EXPOSE 8020

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8020"]
