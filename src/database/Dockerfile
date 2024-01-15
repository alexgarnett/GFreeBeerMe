FROM postgres:16.1
ENV POSTGRES_DB=beer_app
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
COPY ./schema.sql /docker-entrypont-initdb.d/schema.sql
EXPOSE 5432