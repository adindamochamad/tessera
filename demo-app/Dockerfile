FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY pola_query_audit.py .
ENV MONGODB_URI=memory://local
CMD ["uvicorn", "app.main:aplikasi", "--host", "0.0.0.0", "--port", "8081"]
