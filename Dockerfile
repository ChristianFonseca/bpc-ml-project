FROM python:3.11-bookworm

WORKDIR /app

COPY requirements.txt .

COPY src/app.py /app/src/app.py

RUN apt-get update
RUN apt-get install libgomp1 -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "src/app.py"]




