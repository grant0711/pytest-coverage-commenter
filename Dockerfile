FROM alpine:3.11
COPY entrypoint.sh /user/local/entrypoint.sh
#RUN chmod +x entrypoint.sh
ENTRYPOINT ["/user/local/entrypoint.sh"]

