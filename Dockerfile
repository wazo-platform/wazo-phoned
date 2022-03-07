FROM python:3.7-slim-buster AS compile-image
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"

COPY . /usr/src/wazo-phoned
WORKDIR /usr/src/wazo-phoned
RUN pip install -r requirements.txt
RUN python setup.py install

FROM python:3.7-slim-buster AS build-image
COPY --from=compile-image /opt/venv /opt/venv

COPY ./etc/wazo-phoned /etc/wazo-phoned
COPY ./contribs/docker/certs /usr/share/xivo-certs
RUN true \
    && adduser --quiet --system --group --home /var/lib/wazo-phoned wazo-phoned \
    && mkdir -p /etc/wazo-phoned/conf.d \
    && install -o www-data -g www-data /dev/null /var/log/wazo-phoned.log

EXPOSE 9498 9499

# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"
CMD ["wazo-phoned", "-d"]
