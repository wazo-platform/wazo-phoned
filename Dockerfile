FROM python:2.7.13-stretch

RUN apt-get -yq update \
   && apt-get -yqq dist-upgrade \
   && apt-get -yqq install libldap2-dev libsasl2-dev \
   && apt-get -yq autoremove

RUN mkdir -p /etc/xivo-dird-phoned/conf.d

RUN mkdir -p /var/run/xivo-dird-phoned
RUN chmod a+w /var/run/xivo-dird-phoned

RUN touch /var/log/xivo-dird-phoned.log
RUN chown www-data: /var/log/xivo-dird-phoned.log

ADD . /usr/src/xivo-dird-phoned
ADD ./contribs/docker/certs /usr/share/xivo-certs
WORKDIR /usr/src/xivo-dird-phoned
RUN pip install -r requirements.txt
RUN cp -r etc/* /etc

RUN python setup.py install

ONBUILD ADD ./contribs/docker/certs /usr/share/xivo-certs

EXPOSE 9498 9499

CMD ["xivo-dird-phoned", "-fd"]
