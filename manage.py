#!/usr/bin/env python
import os
import sys
from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "registrator.settings")
    from django.core.management import execute_from_command_line
    if hasattr(settings, 'DEVELOPER_HOOK') and settings.DEVELOPER_HOOK.get('ENABLED', None):
        from django.core import management
        from django import setup as django_setup
        django_setup()
        management.call_command('developer_hook')
    execute_from_command_line(sys.argv)
