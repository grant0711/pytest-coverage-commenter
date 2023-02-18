FROM python:3.11-alpine
COPY . /app
WORKDIR /app
#RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/main.py
#ENTRYPOINT ["/app/entrypoint.sh"]
ENTRYPOINT ["/app/main.py"]
