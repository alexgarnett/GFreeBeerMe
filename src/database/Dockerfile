FROM postgres:16.1
ENV POSTGRES_DB=beer_app
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_HOST_AUTH_METHOD=trust
COPY schema.sql /docker-entrypont-initdb.d/schema.sql
EXPOSE 5432