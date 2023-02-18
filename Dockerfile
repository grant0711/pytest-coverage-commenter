FROM python:3.11-alpine
ADD . /app
WORKDIR /app

RUN pip install --target=/app requests

ENV PYTHONPATH /app
#ENTRYPOINT [ "python main.py" ]
CMD ["/app/main.py"]