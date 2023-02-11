FROM alpine:3.11

RUN apk --no-cache add curl

COPY . /app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

