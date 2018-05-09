FROM ubuntu:bionic
MAINTAINER Makina corpus "contact@geotrek.fr"

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /app/requirements

RUN apt-get update && apt-get upgrade -y -qq
ADD requirements/apt.txt /app/requirements/apt.txt
RUN apt-get install $(grep -vE "^\s*#" /app/requirements/apt.txt | tr "\n" " ") -y -qq
RUN apt-get clean all && apt-get autoclean
RUN locale-gen en_US.UTF-8
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && rm get-pip.py
RUN pip install pip setuptools wheel virtualenv --upgrade
RUN useradd -ms /bin/bash django --uid 1001
ADD geotrek /app/geotrek
ADD manage.py /app/manage.py

ADD bulkimport /app/bulkimport

RUN chown django:django -R /app
USER django

RUN virtualenv /app/venv
ADD requirements/pip.txt /app/requirements/pip.txt
RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements/pip.txt

ADD docker /app/docker
RUN mkdir -p /app/public/static /app/public/media /app/public/data
RUN mkdir -p /app/private/cache /app/private/log /app/private/templates

ADD VERSION /app/VERSION
ADD .coveragerc /app/.coveragerc
ADD docker /app/docker
WORKDIR /app
#RUN docker/run.sh
EXPOSE 8000
CMD /app/venv/bin/gunicorn --bind 0.0.0.0:8000