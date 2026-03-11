FROM python:3.12-slim
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY telegram_bot/requirements.txt .
RUN pip install -r requirements.txt
COPY telegram_bot/ /app/
CMD ["python", "main.py"]
