"""
WSGI config for MiniBlogAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

#used for production deployment, not usually needed for development with runserver. (Optional for this Project)

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MiniBlogAPI.settings")

application = get_wsgi_application()
