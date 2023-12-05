FROM python:3.10-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV API_HOST=beer_api
ENV API_PORT=8080
EXPOSE 8000
ENTRYPOINT python main.py