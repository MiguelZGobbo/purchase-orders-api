FROM python:3.11-slim

WORKDIR /app

COPY requirements/ requirements/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
