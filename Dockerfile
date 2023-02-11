FROM alpine:3.10
COPY . /app
#COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["app/entrypoint.sh"]

