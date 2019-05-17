FROM python:3.5-stretch

RUN mkdir -p /etc/wazo-dird-phoned/conf.d

RUN mkdir -p /var/run/wazo-dird-phoned
RUN chmod a+w /var/run/wazo-dird-phoned

RUN touch /var/log/wazo-dird-phoned.log
RUN chown www-data: /var/log/wazo-dird-phoned.log

ADD . /usr/src/wazo-dird-phoned
ADD ./contribs/docker/certs /usr/share/xivo-certs
WORKDIR /usr/src/wazo-dird-phoned
RUN pip install -r requirements.txt
RUN cp -r etc/* /etc

RUN python setup.py install

ADD ./contribs/docker/certs /usr/share/xivo-certs

EXPOSE 9498 9499

CMD ["wazo-dird-phoned", "-fd"]
