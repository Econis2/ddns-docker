#DDNS Image - pyhton + Alpine Linux

FROM alpine:3.8

MAINTAINER Econis "someuser@github.com"

RUN apk add --no-cache python

RUN apk add --no-cache py-requests

RUN mkdir /home/ddns

ADD credentials /home/ddns/credentials

ADD ddns.py /home/ddns/ddns.py

ADD ddns-crontab /etc/cron.d/ddns-cron

RUN chmod 0644 /etc/cron.d/ddns-cron

RUN crontab /etc/cron.d/ddns-cron

RUN touch /var/log/ddns-cron.log

CMD crond -f
