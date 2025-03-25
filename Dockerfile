FROM python:3.13.2-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y tzdata \
    && ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime \
    && echo "Asia/Kolkata" > /etc/timezone \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV TZ=Asia/Kolkata

CMD ["gunicorn", "-w", "1", "run:app", "--bind", "0.0.0.0:5000"]
