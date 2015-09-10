import os
import hashlib
import datetime


def generate_filename(filename):
    hd = hashlib.md5(str(datetime.datetime.now())).hexdigest()
    return os.path.join(hd[:2], hd[2:4], '%s%s' % (hd, os.path.splitext(filename)[1]))


def upload_to_generate_filename(instance, filename):
    return os.path.join(instance.upload_to, generate_filename(filename))
