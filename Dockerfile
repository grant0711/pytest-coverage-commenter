FROM alpine:3.11

COPY --chmod=+x entrypoint.sh /entrypoint.sh



ENTRYPOINT ["/entrypoint.sh"]
