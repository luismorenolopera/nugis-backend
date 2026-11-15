"""
WSGI config for nugis project.

Sentry is initialised in settings.py when SENTRY_DSN is set.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nugis.settings')

application = get_wsgi_application()
