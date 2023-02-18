FROM python:3.11-alpine
COPY . /app
WORKDIR /app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]