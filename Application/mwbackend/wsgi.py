"""
WSGI config for mwbackend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.system('apt install -y libpq-dev python3-dev build-essential')
os.system('pip install psycopg2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mwbackend.settings')

application = get_wsgi_application()
