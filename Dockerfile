FROM python:3.7-buster

RUN mkdir -p /etc/wazo-phoned/conf.d

RUN mkdir -p /var/run/wazo-phoned
RUN chmod a+w /var/run/wazo-phoned

RUN touch /var/log/wazo-phoned.log
RUN chown www-data: /var/log/wazo-phoned.log

ADD . /usr/src/wazo-phoned
ADD ./contribs/docker/certs /usr/share/xivo-certs
WORKDIR /usr/src/wazo-phoned
RUN pip install -r requirements.txt
RUN cp -r etc/* /etc

RUN python setup.py install

ADD ./contribs/docker/certs /usr/share/xivo-certs

EXPOSE 9498 9499

CMD ["wazo-phoned", "-fd"]
