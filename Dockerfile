FROM ubuntu:14.04
MAINTAINER unknownlighter@gmail.com

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
RUN echo "deb http://nginx.org/packages/mainline/ubuntu/ trusty nginx" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
  supervisor \
  nginx \
  gunicorn \
  curl \
  mercurial \
  git \
  python-dev \
  python-virtualenv \
  libgdal-dev \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./docker/id_rsa /root/.ssh/id_rsa

RUN chmod 600 /root/.ssh/id_rsa

RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

ENV work_dir /app

WORKDIR ${work_dir}

RUN virtualenv /env

COPY ./requirements.txt requirements.txt

RUN CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal \
  /env/bin/pip install --process-dependency-links --allow-all-external -r requirements.txt

COPY ./docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./docker/nginx.conf /etc/nginx/conf.d/default.conf

ADD . .

RUN /env/bin/python /app/manage.py collectstatic --noinput

EXPOSE 80

CMD ./docker/docker_start.sh
