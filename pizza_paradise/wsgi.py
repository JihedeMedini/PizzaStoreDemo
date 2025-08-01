"""
WSGI config for pizza_paradise project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza_paradise.settings")

application = get_wsgi_application()

# Add this for Vercel deployment
app = application
