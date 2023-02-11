FROM alpine:3.11
COPY entrypoint.sh /entrypoint.
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

