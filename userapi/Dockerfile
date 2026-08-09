FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy into userapi/ subfolder so "from userapi.src import ..." resolves
COPY . ./userapi/

ENV PYTHONPATH=/app
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=userapi_db
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "2", "--preload", "userapi.src.app:app"]
