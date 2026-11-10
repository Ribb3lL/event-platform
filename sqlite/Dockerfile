FROM alpine:latest
RUN apk add --no-cache sqlite
RUN mkdir -p /dbdata
COPY check-dbs.sh /check-dbs.sh
RUN chmod +x /check-dbs.sh
CMD ["/check-dbs.sh"]
