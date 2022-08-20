FROM python:3.6.9

RUN apt-get update 

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN mkdir -p logs

RUN chmod -R 777 ./logs

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]