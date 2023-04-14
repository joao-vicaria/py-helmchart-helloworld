FROM python:3.10.5-alpine3.16 as prod

RUN mkdir /app
WORKDIR /app
COPY app/* ./
RUN pip install -r requirements.txt
ENV FLASK_APP=main.py
CMD flask run -h 0.0.0.0 -p 5000
