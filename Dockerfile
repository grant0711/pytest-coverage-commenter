FROM python:3.11-alpine
COPY . /app
#WORKDIR /app
RUN pip install --target=/app requests
RUN chmod +x /app/main.py
ENTRYPOINT ["/app/main.py"]
