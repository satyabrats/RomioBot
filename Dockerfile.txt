FROM python:3.10-slim

RUN apt update && apt install -y ffmpeg git build-essential

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
