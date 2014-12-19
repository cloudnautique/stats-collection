FROM dockerbase/cron

MAINTAINER Bill Maxwell <bill@rancher.com>

ADD scripts/bootstrap /tmp/bootstrap
RUN /tmp/bootstrap

VOLUME /scratch
