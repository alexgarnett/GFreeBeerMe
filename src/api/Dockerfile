FROM python:3.10-slim-buster
WORKDIR /api
COPY . .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt
ENV DB_HOST=beer_db
ENV DB_PORT=5432
EXPOSE 8080
ENTRYPOINT python beer_api.py