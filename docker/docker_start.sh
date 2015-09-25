#!/bin/sh

echo resolver $(awk 'BEGIN{ORS=" "} /nameserver/{print $2}' /etc/resolv.conf | sed "s/ $/;/g") > /etc/nginx/resolvers.conf
/env/bin/python manage.py syncdb --noinput 
/env/bin/python manage.py migrate --merge --noinput
/usr/bin/supervisord
