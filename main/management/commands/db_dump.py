# -*- coding: utf-8 -*-
import os
import subprocess
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    args = '<path_to_out_file>'

    option_list = BaseCommand.option_list + (
        make_option('--router', dest='router', action='store', default='default'),
    )

    def handle(self, *args, **options):
        dbs = settings.DATABASES[options.get('router')]
        file_name = '%s.sql' % dbs['NAME']
        if args:
            file_name = args[0]
        file_path = os.path.abspath(file_name)
        cmd = '''export PGPASSWORD={3}; {0} -h {4} -p {5} -U {2} -d {1} -F p -v --clean > {6}'''.format(
            dbs.get('PGDUMP', 'pg_dump'),
            dbs.get('NAME'),
            dbs.get('USER'),
            dbs.get('PASSWORD'),
            dbs.get('HOST'),
            dbs.get('PORT'),
            file_path.replace('.tar.gz', '')
        )
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()
        cmd = '''cd {0}; tar -zcvf {1}.tar.gz {1}; rm {1}'''.format(
            os.path.dirname(file_path),
            os.path.basename(file_path)
        )
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()
