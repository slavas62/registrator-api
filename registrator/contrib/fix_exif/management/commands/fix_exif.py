# coding: utf-8
import os
import logging
from django.core.management.base import BaseCommand
from django.conf import settings

from registrator.contrib.fix_exif import fix_exif

logger = logging.getLogger('console_no_level')


class Command(BaseCommand):
    args = '<path>'

    def handle(self, *args, **options):
        path = args[0] if args else settings.MEDIA_ROOT
        total = 0
        rotate = 0
        skip = 0
        for root, subdirs, files in os.walk(path):
            for f in files:
                total += 1
                i_path = os.path.abspath(os.path.join(root, f))
                r = fix_exif(i_path)
                if r < 1:
                    skip += 1
                    logger.debug('SKIP %s' % i_path)
                else:
                    rotate += 1
                    logger.info('ROTATE %s %s' % (r, i_path))
        logger.warning('\n\nTOTAL %s\nSKIP %s\nROTATE %s' % (total, skip, rotate))
